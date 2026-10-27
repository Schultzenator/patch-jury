"""Run only bundled fixture variants, never model-written source or public PRs."""
import hashlib, json, os, pathlib, subprocess, tempfile, time, uuid
from .fixtures import FIXTURES, expected, validate_cases

IMAGE_FILE = pathlib.Path(__file__).resolve().parent.parent / 'runner-image.txt'
HARNESS = '''import json
from candidate import TARGET
cases = json.load(open('/work/cases.json'))
results=[]
for args in cases:
    try: results.append({'actual':TARGET(*args)})
    except Exception as e: results.append({'error':type(e).__name__})
print(json.dumps(results))
'''

def execute(source, function, cases, timeout=12):
    image=IMAGE_FILE.read_text().strip()
    if '@sha256:' not in image: raise RuntimeError('Runner image must be pinned by digest')
    name='patchjury-'+uuid.uuid4().hex
    with tempfile.TemporaryDirectory(prefix='patchjury-') as temp:
        p=pathlib.Path(temp)
        p.chmod(0o755)
        for filename, content in [('candidate.py',source),('harness.py',HARNESS.replace('TARGET',function)),('cases.json',json.dumps(cases))]:
            (p/filename).write_text(content); (p/filename).chmod(0o644)
        cmd=['docker','run','--rm','--pull=never','--name',name,'--network=none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges','--pids-limit=32','--memory=128m','--memory-swap=128m','--cpus=0.5','--ulimit','nofile=64:64','--user','65534:65534','--mount',f'type=bind,src={p},dst=/work,readonly', '--workdir','/work',image,'python','-B','/work/harness.py']
        started=time.monotonic()
        try:
            proc=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,env={'PATH':os.environ['PATH'],'HOME':os.environ.get('HOME','/tmp')})
        except subprocess.TimeoutExpired:
            subprocess.run(['docker','rm','-f',name],capture_output=True,timeout=5)
            raise RuntimeError('Runner timed out; container removed') from None
        if proc.returncode: raise RuntimeError('Sandbox failed: '+proc.stderr[-1200:])
        values=json.loads(proc.stdout)
        if len(values)!=len(cases): raise RuntimeError('Runner output length mismatch')
        return values, round(time.monotonic()-started,3)

def verdict(variants):
    """A deterministic evidence decision; the model never awards its own score."""
    survivors=[name for name in ['patch_a','patch_b']
               if variants[name]['passed']==variants[name]['total']]
    winner=survivors[0] if len(survivors)==1 else None
    return {'status':'supported' if winner else 'inconclusive',
            'recommended_patch':winner,
            'reason':(winner+' passes every evaluated case; the alternative has counterexamples.'
                      if winner else 'No unique patch passes every evaluated case. Gather more evidence.'),
            'scope':'Evidence from this finite suite only; maintainer approval required.'}

def compare(fixture, cases, provenance):
    f=FIXTURES[fixture]; validate_cases(fixture,cases)
    groups=[('smoke',f['smoke']),('challenge',cases),('held_out',f['hidden'])]
    all_cases=[(group,args) for group,items in groups for args in items]
    report={'fixture':fixture,'title':f['title'],'provenance':provenance,'image':IMAGE_FILE.read_text().strip(), 'variants':{},'limitations':['Bundled fixtures only; no arbitrary repository execution.','Passing finite cases is not proof of correctness.','Oracle is handwritten from the fixture specification.','Held-out cases are excluded from the model prompt but public in this repository.']}
    for variant in ['base','patch_a','patch_b']:
        outputs,seconds=execute(f[variant],f['function'],[args for _,args in all_cases])
        rows=[]
        for (group,args),out in zip(all_cases,outputs):
            want=expected(fixture,args)
            rows.append({'group':group,'args':args,'expected':want,**out,'passed':'actual' in out and type(out['actual']) is type(want) and out['actual']==want})
        report['variants'][variant]={'source':f[variant],'sha256':hashlib.sha256(f[variant].encode()).hexdigest(),'seconds':seconds,'tests':rows,'passed':sum(r['passed'] for r in rows),'total':len(rows)}
    discriminatory=[i for i in range(len(all_cases)) if report['variants']['patch_a']['tests'][i]['passed']!=report['variants']['patch_b']['tests'][i]['passed']]
    report['distinguishing_cases']=discriminatory
    report['challenge_distinguishing_cases']=[i for i in discriminatory if all_cases[i][0]=='challenge']
    report['conclusion']='The evidence distinguishes the patches.' if discriminatory else 'Inconclusive: these cases do not distinguish the patches.'
    report['verdict']=verdict(report['variants'])
    report['report_sha256']=hashlib.sha256(json.dumps(report,sort_keys=True).encode()).hexdigest()
    return report
