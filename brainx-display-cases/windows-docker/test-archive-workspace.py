"""Run in Linux to exercise real POSIX links, with no Docker/model calls."""
import importlib.util
from pathlib import Path
import tarfile
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    'archive_workspace', Path(__file__).with_name('archive-workspace.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ArchiveTests(unittest.TestCase):
    def test_bytes_and_relative_absolute_directory_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'source'; target = root / 'archive'
            (source / 'raw').mkdir(parents=True)
            payload = b'raw\x00bytes\r\n'
            (source / 'raw' / 'data.bin').write_bytes(payload)
            (source / 'relative').symlink_to('raw', target_is_directory=True)
            (source / 'absolute').symlink_to(source / 'raw', target_is_directory=True)
            result = module.archive(source, target)
            for name in ['raw', 'relative', 'absolute']:
                self.assertEqual((target / name / 'data.bin').read_bytes(), payload)
            self.assertTrue((source / 'absolute').is_symlink())
            self.assertEqual((source / 'raw/data.bin').read_bytes(), payload)
            links = [e for e in result['entries'] if e['type'] == 'symlink']
            self.assertTrue(all(e['materialized_view'] for e in links))
            with tarfile.open(target / '.harness-archive/symlinks.tar') as bundle:
                self.assertEqual(bundle.getmember('relative').linkname, 'raw')
                self.assertEqual(bundle.getmember('absolute').linkname, str(source / 'raw'))
                self.assertTrue(all(e.issym() for e in bundle.getmembers()))

    def test_external_broken_and_cyclic_links_do_not_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'source'; source.mkdir()
            (root / 'external.txt').write_text('must not be copied')
            (source / 'external').symlink_to(root / 'external.txt')
            (source / 'broken').symlink_to('missing')
            (source / 'cycle').symlink_to('cycle')
            result = module.archive(source, root / 'archive')
            self.assertTrue(all(not e['materialized_view'] for e in result['entries']))
            self.assertFalse((root / 'archive/external').exists())
            self.assertEqual(len(result['entries']), 3)

    def test_destination_and_reserved_path_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source'; source.mkdir()
            with self.assertRaises(ValueError):
                module.archive(source, source / 'nested')
            with self.assertRaises(ValueError):
                module.archive(source, Path(tmp))
            (source / '.harness-archive').mkdir()
            with self.assertRaises(ValueError):
                module.archive(source, Path(tmp) / 'archive')


if __name__ == '__main__':
    unittest.main()
