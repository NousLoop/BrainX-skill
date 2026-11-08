"""Archive inside Linux: preserve bytes and link metadata; materialize safe views."""
import argparse
import hashlib
import json
import shutil
import tarfile
from pathlib import Path


def archive(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if destination.is_relative_to(source) or source.is_relative_to(destination):
        raise ValueError('Archive and workspace must be disjoint')
    reserved = source / '.harness-archive'
    if reserved.exists() or reserved.is_symlink():
        raise ValueError('Workspace uses reserved .harness-archive path')
    destination.mkdir(parents=True, exist_ok=True)
    metadata = destination / '.harness-archive'
    metadata.mkdir()
    entries, links = [], []
    # rglob does not descend into directory symlinks on Python 3.12.
    for path in sorted(source.rglob('*')):
        relative = path.relative_to(source)
        target = destination / relative
        if path.is_symlink():
            links.append(path)
            entries.append(dict(path=relative.as_posix(), type='symlink',
                                target=str(path.readlink())))
        elif path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            entries.append(dict(path=relative.as_posix(), type='directory'))
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                raise ValueError(f'Archive byte mismatch: {relative}')
            entries.append(dict(path=relative.as_posix(), type='file',
                                bytes=path.stat().st_size, sha256=digest))
        else:
            raise ValueError(f'Unsupported workspace object: {relative}')
    # Regular entries plus these exact link definitions are the lossless archive.
    with tarfile.open(metadata / 'symlinks.tar', 'w') as bundle:
        for path in links:
            bundle.add(path, arcname=path.relative_to(source).as_posix(),
                       recursive=False)

    def materialize(path, target, ancestors=frozenset()):
        try:
            resolved = path.resolve(strict=True)
        except (OSError, RuntimeError):
            return False
        if not resolved.is_relative_to(source) or resolved in ancestors:
            return False
        if resolved.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(resolved, target)
            return True
        if resolved.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            outcomes = [materialize(child, target / child.name,
                                    ancestors | {resolved})
                        for child in resolved.iterdir()]
            return all(outcomes)
        return False

    for entry, path in zip((e for e in entries if e['type'] == 'symlink'), links):
        entry['materialized_view'] = materialize(
            path, destination / path.relative_to(source))
    result = dict(format='regular-files-plus-symlink-tar-v1', entries=entries,
                  note='Symlink paths are materialized views, not original objects. '
                       'Restore canonical links from symlinks.tar in an empty tree '
                       'at the original container mount before scientific replay.')
    (metadata / 'manifest.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('destination')
    args = parser.parse_args()
    result = archive(args.source, args.destination)
    print(json.dumps(dict(entries=len(result['entries']),
                          symlinks=sum(e['type'] == 'symlink'
                                       for e in result['entries']))))
