import unittest
from cableroute.cli import load_case
from cableroute.catalog import *
from cableroute.schedule import *
class CatalogSchedule(unittest.TestCase):
    def test_csv_provenance(self):
        text='id,area_mm2,ampacity_a,r20_ohm_km,x_ohm_km,source,edition,installation,material\nc1,50,140,0.4,0.08,test,2026,test,copper\n'
        rows=import_csv(text);self.assertEqual(rows[0]['area_mm2'],50);self.assertEqual(rows[0]['edition'],'2026')
        with self.assertRaises(ValueError):import_csv(text+'c1,70,180,0.3,0.08,test,2026,test,copper\n')
    def test_neutral_triplen(self):
        m=load_case('example:industrial');harmonics=[{'order':3,'phases':[[40,0]]*3}]
        r=neutral_selection(harmonics,m['catalog'],{'grouping':.8},minimum_area_mm2=35)
        self.assertEqual(r['neutral_current_a'],120);self.assertEqual(r['selected'],'demo-cu-50')
    def test_minimum_policy(self):
        r=neutral_selection([],load_case('example:industrial')['catalog'],minimum_area_mm2=70)
        self.assertEqual(r['selected'],'demo-cu-70')
    def test_schedules(self):
        m=load_case('example:industrial');rows=feeder_schedule([{'id':'=unsafe','model':m}]);text=schedule_csv(rows)
        self.assertIn("'=unsafe",text);self.assertEqual(len(rows),1)
    def test_installation_sensitivity(self):
        rows=installation_sensitivity(load_case('example:industrial'),{'clear':{},'grouped':{'grouping':.5}})
        self.assertGreater(rows[0]['result']['candidates'][0]['ampacity_a'],rows[1]['result']['candidates'][0]['ampacity_a'])
