import tempfile,unittest
from pathlib import Path
class PublicFormsTest(unittest.TestCase):
 def api(self):
  try:from benchmarks import public_forms as f
  except ImportError:self.fail('public Forms preparer missing')
  return f
 def test_packet_binding_and_three_questions(self):
  f=self.api();cases=[{'id':'R001','source':'Nguồn gốc','audience':'Bạn đọc','purpose':'Giải thích'}];outputs={f'codex/R001/{a}':a for a in f.pub.ARMS}
  c,key=f.build_contract(cases,outputs,'A',1)
  self.assertEqual(len(c['questions']),3);self.assertEqual(c['groups'][0]['source'],'Nguồn gốc');self.assertEqual(set(c['groups'][0]['outputs'].values()),set(f.pub.ARMS));self.assertEqual(set(key['Q001']),set('ABCD'));self.assertNotIn('arm',c['groups'][0])
 def test_incomplete_source_outputs_raise(self):
  f=self.api()
  with self.assertRaises(KeyError):f.build_contract([{'id':'R001','source':'Gốc','audience':'Đọc','purpose':'Viết'}],{},'A',1)
 def test_runtime_creates_new_forms_and_has_no_deletion(self):
  f=self.api();s=f.RUNTIME.read_text();self.assertIn('FormApp.create',s);self.assertNotIn('deleteItem',s);self.assertNotIn('1V_gzac9',s);self.assertIn('group_verified',s)
 def test_question_item_order_is_checked(self):
  f=self.api();s=f.RUNTIME.read_text();self.assertIn('sequence drift',s);self.assertIn('getItems().map',s);self.assertIn('contract_digest',s)
if __name__=='__main__':unittest.main()
