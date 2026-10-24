import csv,io
from .engine import design
def feeder_schedule(feeders):
    rows=[];ids=set()
    for feeder in feeders:
        name=feeder['id']
        if name in ids:raise ValueError('Unique feeder IDs required')
        ids.add(name);result=design(feeder['model']);chosen=next((r for r in result['candidates'] if r['id']==result['selected']),None)
        rows.append({'feeder':name,'selected':result['selected'],'current_a':result['design_current_a'],'quantity_m':chosen['quantity_m'] if chosen else None,'loss_kw':chosen['loss_kw'] if chosen else None,'lifecycle_cost':chosen['lifecycle_cost'] if chosen else None})
    return rows
def schedule_csv(rows):
    stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=['feeder','selected','current_a','quantity_m','loss_kw','lifecycle_cost']);writer.writeheader()
    for row in rows:
        safe={k: ("'"+str(v) if isinstance(v,str) and v.startswith(('=','+','-','@')) else v) for k,v in row.items()};writer.writerow(safe)
    return stream.getvalue()
def installation_sensitivity(model,factor_sets):
    return [{'condition':name,'factors':factors,'result':design(dict(model,factors=factors))} for name,factors in factor_sets.items()]
