"""Behavioral tests for this standalone analytical project."""
import importlib.util,math,sqlite3,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from common import queries

def module(slug):
    spec=importlib.util.spec_from_file_location(slug,ROOT/'analyze.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def fixture(slug,table,rows):
    m=module(slug);db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    db.execute('CREATE TABLE '+table+' ('+m.SCHEMA+')')
    db.executemany('INSERT INTO '+table+' VALUES ('+','.join('?' for _ in rows[0])+')',rows)
    return queries(db,ROOT/'analysis.sql')

class AnalystTests(unittest.TestCase):
    def test_identical_variants_are_inconclusive(self):
        s=module('03-marketing-experiment').compare(100,1000,100,1000)
        self.assertEqual(s['two_sided_p'],1);self.assertEqual(s['decision'],'Inconclusive')
    def test_large_lift_and_interval(self):
        s=module('03-marketing-experiment').compare(100,1000,200,1000)
        self.assertGreater(s['ci_low_pp'],0);self.assertEqual(s['decision'],'Evidence of improvement')
        self.assertAlmostEqual(s['lift_pp'],10)
    def test_assignment_mismatch_blocks_decision(self):
        s=module('03-marketing-experiment').compare(100,1000,50,200)
        self.assertEqual(s['decision'],'Investigate assignment')
    def test_small_counts_and_invalid_inputs(self):
        f=module('03-marketing-experiment').compare
        self.assertEqual(f(0,100,0,100)['decision'],'Insufficient counts')
        with self.assertRaises(ValueError):f(1,0,2,100)
    def test_full_analysis_runs_and_exports(self):
        result=module('standalone').run()
        self.assertTrue(result)
        self.assertTrue((ROOT/'index.html').is_file())
        self.assertTrue((ROOT/'results/metrics.json').is_file())
if __name__=='__main__':unittest.main()
