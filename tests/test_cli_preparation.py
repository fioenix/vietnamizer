import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from tests.test_coverage import raw

class CLITest(unittest.TestCase):
    def run_cli(self,doc,command='prepare',extra=()):
        env={k:v for k,v in os.environ.items() if k!='TYPESAFE_API_KEY'}
        return subprocess.run([sys.executable,'-B','-m','jev',command,*extra],input=json.dumps(doc),text=True,capture_output=True,env=env)
    def test_prepare_offline_is_not_evaluation(self):
        r=self.run_cli(raw())
        self.assertEqual(r.returncode,0,r.stderr)
        a=json.loads(r.stdout)
        self.assertEqual(a['status'],'prepared')
        self.assertFalse(a['evaluation_complete'])
        self.assertEqual(a['counts']['sentences'],2)
        self.assertNotIn('Tôi về',r.stdout)
    def test_unresolved_prepare_exits_2(self):
        r=self.run_cli(raw('Tôi chưa biết… Có lẽ mai.'))
        self.assertEqual(r.returncode,2)
        self.assertEqual(json.loads(r.stdout)['status'],'preparation_incomplete')
    def test_no_key_evaluate_does_not_read_invalid_file(self):
        env={k:v for k,v in os.environ.items() if k!='TYPESAFE_API_KEY'}
        r=subprocess.run([sys.executable,'-B','-m','jev','evaluate','--input','/nonexistent'],capture_output=True,text=True,env=env)
        self.assertEqual(r.returncode,0)
        self.assertEqual(json.loads(r.stdout)['status'],'key_absent')
