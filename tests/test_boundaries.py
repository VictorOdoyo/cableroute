import unittest,copy
from cableroute.engine import *
from cableroute.cli import load_case
from cableroute.studies import run
class Boundaries(unittest.TestCase):
    def test_bad_factors(self):
        for args in [(10,0),(10,400,0),(10,400,1.1),(10,400,1,2)]:
            with self.assertRaises(ValueError):demand_current(*args)
    def test_invalid_numbers(self):
        for v in [float('nan'),float('inf'),-1,True]:
            with self.assertRaises(ValueError):thermal_area(v,1,115)
    def test_no_feasible(self):
        m=load_case('example:industrial');m['load']['power_kw']=10000
        self.assertIsNone(design(m)['selected'])
    def test_source_required(self):
        m=load_case('example:industrial');del m['catalog'][0]['source']
        with self.assertRaises(ValueError):design(m)
    def test_fault_sharing_conservative(self):
        m=load_case('example:industrial');m['parallel_runs']=2;m['fault']['current_a']=20000
        conservative=design(m);m['equal_fault_sharing']=True;shared=design(m)
        self.assertFalse(conservative['candidates'][0]['checks']['thermal'])
        self.assertTrue(shared['candidates'][-1]['checks']['thermal'])
    def test_neutral_duplicate(self):
        row={'order':3,'phases':[[1,0]]*3}
        with self.assertRaises(ValueError):harmonic_neutral([row,row])
    def test_parallel_kcl(self):
        values=parallel_share(100,[[.1,.2],[.2,.1],[.3,.4]])
        self.assertAlmostEqual(abs(sum(values)-100),0)
    def test_provenance(self):
        m=load_case('example:industrial');r=run(m);r2=run(m)
        self.assertEqual(r['provenance'],r2['provenance']);m['length_m']+=1
        self.assertNotEqual(r['provenance']['model_sha256'],run(m)['provenance']['model_sha256'])
    def test_sensitivity(self):
        rows=run(load_case('example:industrial'),'sensitivity')['temperatures']
        self.assertLess(rows[0]['result']['candidates'][0]['loss_kw'],rows[-1]['result']['candidates'][0]['loss_kw'])
    def test_zero_horizon(self):self.assertEqual(lifecycle(100,1,1000,.2,0),100)
