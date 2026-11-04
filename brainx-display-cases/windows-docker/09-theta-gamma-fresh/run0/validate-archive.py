"""Check archive identity, raw review preservation, and secrets without printing secrets."""
import hashlib
import json
from pathlib import Path
import re
import subprocess


root = Path(__file__).resolve().parent
repo = root.parents[3]
env = repo / 'brainx-display-cases/windows-docker/brainx-eval.env'
config = env.read_text(encoding='utf-8')
credential = re.search(r'^OPENAI_API_KEY="([^"]+)"', config, re.M).group(1).encode()
folders = [root.parent, root.parent.parent / '00-live-model-probe']
secret_hits = []
inventory = {}
for folder in folders:
    for path in sorted(folder.rglob('*')):
        if not path.is_file():
            continue
        data = path.read_bytes()
        relative = str(path.relative_to(repo)).replace('\\', '/')
        if credential in data or re.search(rb'sk-magpie-key-[0-9a-f]{24,}', data):
            secret_hits.append(relative)
        if path.is_relative_to(root / 'theta_gamma'):
            inventory[str(path.relative_to(root))] = hashlib.sha256(data).hexdigest()
assert not secret_hits, 'Credential found in archive; do not commit'

calls = []
event_types = {}
for line in (root / 'codex-events.jsonl').read_text(encoding='utf-8').splitlines():
    event = json.loads(line)
    event_types[event['type']] = event_types.get(event['type'], 0) + 1
    item = event.get('item', {})
    if item.get('type') == 'mcp_tool_call' and item.get('status') == 'completed':
        calls.append(item)
assert len(calls) == 2
review_checks = []
for number, call in enumerate(calls, 1):
    returned = call['result']['structured_content']['content']
    saved = (root / f'theta_gamma/reviews/iteration-{number}.md').read_text(encoding='utf-8')
    assert returned == saved, f'Review {number} was not saved verbatim'
    review_checks.append({'iteration': number, 'verbatim': True,
                          'tool': call['tool'], 'error': call.get('error'),
                          'threadId': call['result']['structured_content']['threadId']})
prompt = (root.parent / 'prompt.md').read_bytes()
assert prompt == (root / 'harness-prompt.md').read_bytes()
assert not (root.parent / 'run1').exists()
staged = subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=repo).split(b'\0')
index_verified = 0
for record in staged:
    if not record:
        continue
    entry, name = record.split(b'\t', 1)
    path = name.decode('utf-8')
    if not any(path.startswith(str(folder.relative_to(repo)).replace('\\', '/') + '/')
               for folder in folders):
        continue
    # A blob SHA includes its canonical Git object header, not text normalization.
    data = (repo / path).read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert actual == entry.split()[1].decode(), f'Git index changed archive bytes: {path}'
    index_verified += 1
receipt = {'status': 'PASS', 'credential_scan': 'no matches',
           'prompt_bytes': len(prompt), 'prompt_sha256': hashlib.sha256(prompt).hexdigest(),
           'raw_reviews': review_checks, 'event_counts': event_types,
           'generated_tree_sha256': inventory, 'run1_absent': True,
           'git_index_blobs_exact': index_verified}
(root / 'outer-audit/archive-validation.json').write_text(json.dumps(receipt, indent=2))
print(json.dumps({k: v for k, v in receipt.items() if k != 'generated_tree_sha256'}, indent=2))
