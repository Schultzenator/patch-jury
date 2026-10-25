import concurrent.futures, json, os, pathlib, tempfile, unittest
from unittest.mock import patch
from patchjury.fixtures import FIXTURES, expected, validate_cases
from patchjury.provider import Budget, generate, MODEL
from patchjury.runner import compare, execute

class ValidationTests(unittest.TestCase):
    def test_reject_code_booleans_invalid_domains_and_duplicates(self):
        for key,cases in [('pages',[[True,1]]),('pages',[[2,0]]),('money',[['__import__("os")']]),('intervals',[[[1,1],[0,1]]]),('pages',[[1,2],[1,2]]),('pages',[]),('pages',[[1,2]]*13)]:
            with self.subTest(key=key,cases=cases), self.assertRaises(ValueError): validate_cases(key,cases)
    def test_oracles(self):
        self.assertEqual(expected('pages',[0,2]),0)
        self.assertEqual(expected('money',['1.005']),101)
        self.assertFalse(expected('intervals',[[0,1],[1,2]]))
    def test_all_examples_valid(self):
        for k,f in FIXTURES.items(): validate_cases(k,f['examples'])

class BudgetTests(unittest.TestCase):
    def test_atomic_cap_and_persistence(self):
        with tempfile.TemporaryDirectory() as d:
            path=pathlib.Path(d)/'budget.db'; b=Budget(path)
            for _ in range(995): b.reserve()
            def attempt(_):
                try: b.reserve(); return True
                except ValueError: return False
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                self.assertEqual(sum(pool.map(attempt,range(20))),5)
            self.assertEqual(Budget(path).status()['reserved_usd'],10)
            with self.assertRaises(ValueError): Budget(path).reserve()
    def test_no_call_without_free_credit_confirmation(self):
        with patch.dict(os.environ,{'NEBIUS_CREDITS_CONFIRMED':'no'},clear=True),patch('urllib.request.urlopen') as request:
            with self.assertRaises(ValueError): generate('pages')
            request.assert_not_called()
    def test_live_contract_and_no_patches_in_prompt(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def read(self,*args): return json.dumps({'model':MODEL,'id':'unit-test-only','usage':{'prompt_tokens':100,'completion_tokens':20},'choices':[{'message':{'content':'{"cases": [[0, 10], [20, 10]]}'}}]}).encode()
        with tempfile.TemporaryDirectory() as d,patch.dict(os.environ,{'NEBIUS_API_KEY':'unit-test-not-a-key','NEBIUS_CREDITS_CONFIRMED':'yes'}),patch('urllib.request.urlopen') as request:
            catalog_response=unittest.mock.MagicMock()
            catalog_response.__enter__.return_value.read.return_value=json.dumps([{'flavors':[{'model_id':MODEL,'input_price_per_million_tokens':0.06,'output_price_per_million_tokens':0.24}]}]).encode()
            request.side_effect=[catalog_response,Response()]
            cases,provenance=generate('pages',Budget(pathlib.Path(d)/'budget.db'))
            self.assertEqual(cases,[[0,10],[20,10]])
            self.assertEqual(provenance['usage']['completion_tokens'],20)
            payload=json.loads(request.call_args.args[0].data)
            self.assertNotIn(FIXTURES['pages']['patch_b'],payload['messages'][0]['content'])
            self.assertEqual(payload['max_tokens'],4096)
            self.assertEqual(request.call_count,2)

@unittest.skipUnless(os.environ.get('PATCHJURY_INTEGRATION')=='1','Set PATCHJURY_INTEGRATION=1 for Docker tests')
class SandboxTests(unittest.TestCase):
    def test_regressions(self):
        for key,f in FIXTURES.items():
            with self.subTest(fixture=key):
                r=compare(key,f['examples'],{'mode':'test'})
                self.assertFalse(r['variants']['base']['tests'][0]['passed'])
                self.assertTrue(r['variants']['patch_a']['tests'][0]['passed'])
                self.assertEqual(r['variants']['patch_b']['passed'],r['variants']['patch_b']['total'])
                self.assertTrue(r['distinguishing_cases'])
    def test_no_host_secrets_no_network_readonly_nonroot(self):
        source='''import os,socket
 def_placeholder
'''.replace(' def_placeholder','''def probe():
    results={"uid":os.getuid(),"secret":os.environ.get("NEBIUS_API_KEY"),"home_visible":os.path.exists("/home/schultze/Factory")}
    try:
        open("/escape", "w").write("bad")
        results["write"]=True
    except OSError: results["write"]=False
    try:
        s=socket.create_connection(("1.1.1.1",443),timeout=1);s.close();results["network"]=True
    except OSError: results["network"]=False
    return results
''')
        values,_=execute(source,'probe',[[]])
        self.assertEqual(values[0]['actual'],{'uid':65534,'secret':None,'home_visible':False,'write':False,'network':False})
    def test_timeout_cleanup(self):
        with self.assertRaisesRegex(RuntimeError,'timed out'): execute('def spin():\n    while True: pass\n','spin',[[]],timeout=1)

if __name__=='__main__': unittest.main()
