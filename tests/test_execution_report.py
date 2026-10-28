import unittest
from benchmarks import execution_report as r

class ExecutionReportTests(unittest.TestCase):
    def test_small_nonzero_change_is_not_labelled_unchanged(self):
        self.assertEqual(r.change_label(0),'0.0%')
        self.assertEqual(r.change_label(.0001),'<0,1%')
        self.assertEqual(r.change_label(.01),'1.0%')

    def test_corpus_cannot_drift_even_if_two_copies_match(self):
        original={'cases':[{'id':'R001','source':'Gốc'}]}
        manifest={'corpus_digest':r.pilot.digest(original)}
        r.verify_corpus(original,manifest,original)
        changed={'cases':[{'id':'R001','source':'Đã thay'}]}
        with self.assertRaises(ValueError):r.verify_corpus(changed,manifest,changed)

    def test_identical_and_format_only_are_distinct(self):
        self.assertEqual(r.metrics('Tiếng Việt','Tiếng Việt')['character_change'],0)
        m=r.metrics('Xin  chào\nViệt Nam','Xin chào Việt Nam')
        self.assertFalse(m['unchanged_raw'])
        self.assertTrue(m['unchanged_whitespace_collapsed'])
        self.assertGreater(m['character_change'],0)
        self.assertEqual(m['character_change_whitespace_collapsed'],0)

    def test_length_counts_unicode_codepoints_not_bytes(self):
        m=r.metrics('á🙂','á🙂!')
        self.assertEqual(m['source_chars'],2)
        self.assertEqual(m['output_chars'],3)
        self.assertEqual(m['length_change_pct'],50)
        self.assertFalse(m['unchanged_raw'])

    def test_empty_text_rejected(self):
        for a,b in [('', 'a'),('a',''),(' ','a')]:
            with self.assertRaises(ValueError):r.metrics(a,b)

    def test_summary_uses_twenty_sources_and_no_token_double_count(self):
        rows=[{'runtime':'codex','arm':'vietnamizer','source_id':f'R{n:03}',
               **r.metrics('á','á!'),'seconds':n,'input_tokens':10,'output_tokens':5,'reasoning_tokens':3} for n in range(1,21)]
        s=r.summarize(rows)[0]
        self.assertEqual(s['n_sources'],20)
        self.assertEqual(s['seconds']['median'],10.5)
        self.assertEqual(s['input_tokens']['sum'],200)
        self.assertEqual(s['output_tokens']['sum'],100)
        self.assertNotIn('total_tokens',s)
        with self.assertRaises(ValueError):r.summarize(rows+[rows[0]])

if __name__=='__main__':unittest.main()
