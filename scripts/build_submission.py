"""Build an allowlisted public test archive; never export account evidence or logs."""
import hashlib, pathlib, tarfile
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/'demo/submission/patch-jury-submission.tar.gz'
files=[ROOT/x for x in ['README.md','LICENSE','.env.example','.gitignore','package.json','package-lock.json','tsconfig.json','runner-image.txt','SUBMISSION-KIT.md']]
for directory in ['patchjury','web','tests','scripts','docs']:
    files.extend(p for p in (ROOT/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
files.extend(ROOT/'evidence'/x for x in ['pages.json','money.json','intervals.json','submission-pages.json','model-catalog-20261027.json','final-test-output.txt'])
files.extend([ROOT/'demo/README.md',ROOT/'demo/submission-narration.txt'])
files.extend(p for p in OUT.parent.iterdir() if p.suffix in ['.png','.mp4','.ffconcat'])
with tarfile.open(OUT,'w:gz') as archive:
    for p in sorted(files): archive.add(p,arcname=str(p.relative_to(ROOT)),recursive=False)
sha=hashlib.sha256(OUT.read_bytes()).hexdigest()
OUT.with_suffix(OUT.suffix+'.sha256').write_text(sha+'  '+OUT.name+'\n')
print(OUT.relative_to(ROOT),OUT.stat().st_size,'bytes',sha)
