"""Submission boundary tests: configuration, fail-closed provider and verdict."""
import json
import os
import pathlib
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import urllib.error
from patchjury.provider import Budget, configuration, generate, MODEL
from patchjury.runner import verdict

class SubmissionTests(unittest.TestCase):
    def test_env_routing_and_model_reach_request_and_provenance(self):
        model='nvidia/test-nemotron'
        def response(data):
            r=MagicMock(); r.__enter__.return_value.read.return_value=json.dumps(data).encode(); return r
        catalog=[{'flavors':[{'model_id':model,'input_price_per_million_tokens':.06,'output_price_per_million_tokens':.24}]}]
        answer={'model':model,'id':'contract-only','usage':{'completion_tokens':12},'choices':[{'message':{'content':'{"cases":[[0,10],[11,10],[20,10]]}'}}]}
        env={'NEBIUS_API_KEY':'placeholder-not-a-key','NEBIUS_CREDITS_CONFIRMED':'yes','NEBIUS_BASE_URL':'https://example.test/v1/','MODEL':model}
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ,env,clear=True), patch('urllib.request.urlopen',side_effect=[response(catalog),response(answer)]) as call:
            cases,provenance=generate('pages',Budget(pathlib.Path(d)/'ledger'))
            request=call.call_args.args[0]
            self.assertEqual(request.full_url,'https://example.test/v1/chat/completions')
            self.assertEqual(json.loads(request.data)['model'],model)
            self.assertEqual(provenance['model'],model)
            self.assertEqual(provenance['request_id'],'contract-only')
            self.assertNotIn(env['NEBIUS_API_KEY'],json.dumps(provenance))
            self.assertEqual(len(cases),3)

    def test_config_rejects_invalid_endpoint_or_non_nvidia(self):
        for base in ['http://example.test/v1','https://user:key@example.test/v1','https://example.test/v1?key=x','https://example.test/v1/chat/completions']:
            with self.subTest(base=base), patch.dict(os.environ,{'NEBIUS_BASE_URL':base},clear=True), self.assertRaises(ValueError): configuration()
        with patch.dict(os.environ,{'MODEL':'other/model'},clear=True), self.assertRaises(ValueError): configuration()

    def test_price_change_blocks_before_reservation_and_inference(self):
        response=MagicMock(); response.__enter__.return_value.read.return_value=json.dumps([{'flavors':[{'model_id':MODEL,'input_price_per_million_tokens':.07,'output_price_per_million_tokens':.24}]}]).encode()
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ,{'NEBIUS_API_KEY':'placeholder','NEBIUS_CREDITS_CONFIRMED':'yes'},clear=True), patch('urllib.request.urlopen',return_value=response) as call:
            budget=Budget(pathlib.Path(d)/'ledger')
            with self.assertRaisesRegex(ValueError,'pricing changed'): generate('pages',budget)
            self.assertEqual(budget.status()['attempts'],0)
            self.assertEqual(call.call_count,1)

    def test_failed_live_attempts_stay_reserved_and_never_fall_back(self):
        catalog=[{'flavors':[{'model_id':MODEL,'input_price_per_million_tokens':.06,'output_price_per_million_tokens':.24}]}]
        def response(data):
            r=MagicMock(); r.__enter__.return_value.read.return_value=json.dumps(data).encode(); return r
        for failure in [urllib.error.URLError('timeout'),
                        {'model':MODEL,'choices':[{'message':{'content':'not JSON'}}]},
                        {'model':'other/model','choices':[]}]:
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as d, patch.dict(os.environ,{'NEBIUS_API_KEY':'placeholder','NEBIUS_CREDITS_CONFIRMED':'yes'},clear=True):
                budget=Budget(pathlib.Path(d)/'ledger')
                effect=failure if isinstance(failure,Exception) else response(failure)
                with patch('urllib.request.urlopen',side_effect=[response(catalog),effect]) as call:
                    with self.assertRaises((ValueError,urllib.error.URLError)):
                        generate('pages',budget)
                    self.assertEqual(call.call_count,2)  # no automatic retry
                self.assertEqual(budget.status()['attempts'],1)
                self.assertEqual(budget.status()['reserved_usd'],.01)

    def test_unique_survivor_only_and_no_automatic_merge(self):
        for a,b,winner in [(3,9,'patch_b'),(9,3,'patch_a'),(9,9,None),(3,4,None)]:
            with self.subTest(a=a,b=b):
                result=verdict({'patch_a':{'passed':a,'total':9},'patch_b':{'passed':b,'total':9}})
                self.assertEqual(result['recommended_patch'],winner)
                self.assertEqual(result['status'],'supported' if winner else 'inconclusive')
