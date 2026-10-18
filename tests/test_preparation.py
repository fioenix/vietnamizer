import json
from pathlib import Path
import unittest
from jev.preparation import prepare_document

class CorpusTests(unittest.TestCase):
    def test_independently_annotated_cases(self):
        corpus=json.loads(Path('tests/fixtures/segmentation/cases.json').read_text())
        for case in corpus['cases']:
            with self.subTest(case=case['id']):
                doc={'schema_version':2,'source':{'id':'article','layout':case['layout'],'text':case['text']},'defaults':{'profile':'blog'},'annotations':[{'start':a,'end':b,'protected':True} for a,b in case.get('protected_spans',[])],'boundary_overrides':case.get('boundary_overrides',[])}
                got=prepare_document(doc)
                exact=[[s['source_start']+t['start'],s['source_start']+t['end']] for s in got['sections'] for t in s['sentences'] if t['boundary_status']=='exact']
                self.assertEqual(case['sentences'],exact)
                self.assertEqual(case['unresolved'],not got['segmentation_complete'])
                self.assertEqual(case['text'],''.join(case['text'][p['start']:p['end']] for p in got['partition']))
                parents=[[s['source_start'],s['source_end']] for s in got['sections'] if s['kind'] in ('prose','list')]
                self.assertEqual(case['parents'],parents)
