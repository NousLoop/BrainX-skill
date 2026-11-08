from pathlib import Path
import os,re,json,hashlib
case=Path('brainx-display-cases/windows-docker/19-brunel-lif-regimes')
key=os.environ.get('OPENAI_API_KEY','').encode()
hits=[];scanned=0
for p in case.rglob('*'):
 if p.is_file() and p.suffix in ['.md','.txt','.json','.jsonl','.log','.py','.sh','.toml','.html']:
  data=p.read_bytes();scanned+=1
  if (key and key in data) or re.search(rb'sk-magpie-key-[0-9a-f]{24,}|sk-[A-Za-z0-9_-]{30,}',data):hits.append(str(p.relative_to(case)))
original=(case/'prompt.md').read_bytes()
assert original==Path('brainx-display-cases/legacy-macos/19-brunel-lif-regimes/prompt.md').read_bytes()
result=dict(text_files_scanned=scanned,credential_matches=hits,original_prompt_sha256=hashlib.sha256(original).hexdigest(),original_prompt_unchanged=True)
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result));assert not hits
