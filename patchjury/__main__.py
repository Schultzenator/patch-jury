import argparse, json, pathlib
from .fixtures import FIXTURES
from .runner import compare
from .provider import generate

def main():
    parser=argparse.ArgumentParser(description='Patch Jury: compare bundled regression fixes')
    parser.add_argument('--fixture',choices=FIXTURES,default='pages')
    parser.add_argument('--live',action='store_true')
    parser.add_argument('--output',default='report.json')
    parser.add_argument('--serve',action='store_true')
    args=parser.parse_args()
    if args.serve:
        from .server import serve
        serve(); return
    f=FIXTURES[args.fixture]
    if args.live: cases,provenance=generate(args.fixture)
    else: cases,provenance=f['examples'],{'mode':'authored-example','model':None,'note':'Hand-authored cases, not an API recording or live inference.'}
    print('PATCH JURY | '+f['title'],flush=True)
    print('Provenance: '+provenance['mode'],flush=True)
    report=compare(args.fixture,cases,provenance)
    for name,v in report['variants'].items():
        print(f"{name:8}  {v['passed']}/{v['total']} passed | {v['seconds']}s")
        for t in v['tests']:
            print(f"  {'PASS' if t['passed'] else 'FAIL'} {t['group']:9} {t['args']} -> {t.get('actual',t.get('error'))!r} (expected {t['expected']!r})")
    print(report['conclusion'])
    print('Verdict: '+report['verdict']['status']+' | '+report['verdict']['reason'])
    pathlib.Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
    print('Evidence exported: '+args.output)
if __name__=='__main__': main()
