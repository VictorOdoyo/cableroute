import numpy as np
from cableroute.engine import *
def verify(test,c):
    kind=c['kind'];args=c['inputs'];expected=c['expected']
    functions={'demand':demand_current,'drop':voltage_drop,'thermal':thermal_area,'resistance':resistance_at,'ampacity':corrected_ampacity,'neutral':harmonic_neutral,'lifecycle':lifecycle,'protective':protective_conductor}
    if kind=='parallel':actual=[[z.real,z.imag] for z in parallel_share(*args)]
    elif kind=='selection':actual=[r['feasible'] for r in design(*args)['candidates']]
    else:actual=functions[kind](*args)
    if isinstance(expected,dict):
        for key in expected:np.testing.assert_allclose(actual[key],expected[key],rtol=1e-8,atol=1e-8)
    else:np.testing.assert_allclose(actual,expected,rtol=1e-8,atol=1e-8)
