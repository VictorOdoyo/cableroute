"""Project catalog import and discrete conductor selection; no normative tables."""
import csv,io,json
from .engine import number,corrected_ampacity,harmonic_neutral,thermal_area
def import_csv(text):
    rows=list(csv.DictReader(io.StringIO(text)))
    required={'id','area_mm2','ampacity_a','r20_ohm_km','x_ohm_km','source','edition','installation','material'}
    if not rows or not required.issubset(rows[0]):raise ValueError('Missing required catalog columns')
    ids=set()
    for row in rows:
        if not row['id'] or row['id'] in ids:raise ValueError('Catalog IDs must be unique')
        ids.add(row['id'])
        for key in ['area_mm2','ampacity_a','r20_ohm_km','x_ohm_km','cost_per_m','alpha']:
            if key in row and row[key]!='':row[key]=number(float(row[key]),key,strict=key in ('area_mm2','ampacity_a'))
            elif key in row:del row[key]
        for key in ['source','edition','installation','material']:
            if not row[key].strip():raise ValueError('Catalog provenance must be nonempty')
    return rows

def neutral_selection(harmonics,candidates,factors=None,minimum_area_mm2=0,fault=None):
    current=harmonic_neutral(harmonics);minimum=number(minimum_area_mm2,'minimum area')
    if fault:minimum=max(minimum,thermal_area(fault['current_a'],fault['seconds'],fault['k']))
    rows=[]
    for cable in candidates:
        if not cable.get('source') or not cable.get('edition'):raise ValueError('Neutral candidate provenance required')
        area=number(cable['area_mm2'],'area',strict=True);ampacity=corrected_ampacity(cable['ampacity_a'],factors or {})
        rows.append({'id':cable['id'],'area_mm2':area,'ampacity_a':ampacity,'feasible':area>=minimum and ampacity>=current})
    feasible=[r for r in rows if r['feasible']]
    return {'neutral_current_a':current,'minimum_area_mm2':minimum,'candidates':rows,'selected':min(feasible,key=lambda r:r['area_mm2'])['id'] if feasible else None,'assumption':'User sets project-specific minimum area and correction policy; no automatic neutral reduction rules.'}
