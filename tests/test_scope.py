import unittest
from cableroute.engine import demand_current,thermal_area,design
from cableroute.cli import load_case
class Scope(unittest.TestCase):
    def test_thermal_duration(self):
        with self.assertRaises(ValueError):thermal_area(1000,6,115)
    def test_duplicate_ids(self):
        m=load_case('example:industrial');m['catalog'][1]['id']=m['catalog'][0]['id']
        with self.assertRaises(ValueError):design(m)
    def test_boolean_phase(self):
        with self.assertRaises(ValueError):demand_current(10,230,1,True)
