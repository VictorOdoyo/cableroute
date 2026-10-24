"""SI-derived cable calculations; catalog ratings are supplied, never normative defaults."""
import math
import cmath

def number(value,name,minimum=0,strict=False):
    if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value) or (value<=minimum if strict else value<minimum):
        raise ValueError(f'{name} must be finite and {">" if strict else ">="} {minimum}')
    return float(value)

def demand_current(power_kw,voltage_v,pf=1,phases=3,efficiency=1,demand=1):
    p=number(power_kw,'power');v=number(voltage_v,'voltage',strict=True)
    f=number(pf,'power factor',strict=True);e=number(efficiency,'efficiency',strict=True);d=number(demand,'demand')
    if f>1 or e>1 or d>1 or isinstance(phases,bool) or phases not in (1,3):raise ValueError('Invalid factor or phase count')
    return p*1000*d/(v*f*e*(math.sqrt(3) if phases==3 else 1))

def resistance_at(r20,temperature,alpha=.00393):
    r=number(r20,'resistance');a=number(alpha,'alpha')
    if not isinstance(temperature,(int,float)) or not math.isfinite(temperature) or 1+a*(temperature-20)<=0:raise ValueError('Invalid conductor temperature')
    return r*(1+a*(temperature-20))

def corrected_ampacity(rating,factors):
    value=number(rating,'ampacity',strict=True)
    for name,f in factors.items():value*=number(f,str(name),strict=True)
    return value

def voltage_drop(current,length_m,r_ohm_km,x_ohm_km,pf,voltage_v,phases=3,leading=False):
    i=number(current,'current');l=number(length_m,'length')/1000;r=number(r_ohm_km,'resistance');x=number(x_ohm_km,'reactance')
    f=number(pf,'power factor');v=number(voltage_v,'voltage',strict=True)
    if f>1 or phases not in (1,3):raise ValueError('Invalid power factor or phases')
    drop=(math.sqrt(3) if phases==3 else 2)*i*l*(r*f+(-1 if leading else 1)*x*math.sqrt(1-f*f))
    return {'volts':drop,'percent':100*drop/v}

def thermal_area(fault_a,seconds,k):
    if number(seconds,'duration')>5:raise ValueError('Adiabatic duration is limited to 5 seconds; use a transient thermal model for longer faults')
    return number(fault_a,'fault current')*math.sqrt(number(seconds,'duration'))/number(k,'adiabatic k',strict=True)

def parallel_share(current,impedances):
    number(current,'current')
    if not impedances:raise ValueError('At least one parallel path required')
    zs=[complex(*z) for z in impedances]
    if any(not math.isfinite(z.real) or not math.isfinite(z.imag) or z.real<0 or abs(z)==0 for z in zs):raise ValueError('Invalid path impedance')
    y=sum(1/z for z in zs)
    if abs(y)<1e-15:raise ValueError('Parallel admittance cancels')
    return [current/z/y for z in zs]

def harmonic_neutral(harmonics):
    """Rows contain order and three RMS complex phasors [real,imag]."""
    total=0
    orders=set()
    for row in harmonics:
        h=row['order']
        if isinstance(h,bool) or not isinstance(h,int) or h<1 or h in orders:raise ValueError('Harmonic orders must be unique positive integers')
        orders.add(h)
        if len(row['phases'])!=3:raise ValueError('Three phase phasors required')
        values=[complex(*z) for z in row['phases']]
        if any(not math.isfinite(z.real) or not math.isfinite(z.imag) for z in values):raise ValueError('Nonfinite phasor')
        total+=abs(sum(values))**2
    return math.sqrt(total)

def lifecycle(capital,loss_kw,hours,tariff,years,discount=0):
    for key,value in locals().copy().items():number(value,key)
    if years!=int(years):raise ValueError('Years must be integer')
    annual=loss_kw*hours*tariff
    return capital+sum(annual/(1+discount)**year for year in range(1,int(years)+1))

def design(model):
    load=model['load'];current=demand_current(**load)
    length=number(model['length_m'],'length');temp=model.get('temperature_c',70)
    fault=model['fault'];required=thermal_area(fault['current_a'],fault['seconds'],fault['k'])
    if not fault.get('k_source'):raise ValueError('Document the adiabatic k source and temperature basis')
    factors=model.get('factors',{})
    limit=number(model.get('drop_limit_percent',5),'drop limit',strict=True)
    protective=number(model.get('protective_rating_a',current),'protective rating',strict=True)
    n=model.get('parallel_runs',1)
    if isinstance(n,bool) or not isinstance(n,int) or not 1<=n<=64:raise ValueError('parallel_runs must be 1..64')
    rows=[]
    if not model.get('catalog'):raise ValueError('Catalog is empty')
    ids=[row['id'] for row in model['catalog']]
    if any(not isinstance(key,str) or not key.strip() for key in ids) or len(ids)!=len(set(ids)):raise ValueError('Catalog IDs must be nonempty unique strings')
    for cable in model['catalog']:
        for key in ('source','edition','installation','material'):
            if not cable.get(key):raise ValueError(f'Catalog entry needs {key}')
        area=number(cable['area_mm2'],'area',strict=True)
        amp=corrected_ampacity(cable['ampacity_a'],factors)*n
        r=resistance_at(cable['r20_ohm_km'],temp,cable.get('alpha',.00393))
        drop=voltage_drop(current/n,length,r,cable['x_ohm_km'],load.get('pf',1),load['voltage_v'],load.get('phases',3),model.get('leading',False))
        loss=(3 if load.get('phases',3)==3 else 2)*(current/n)**2*r*length/1000*n/1000
        # Equal fault sharing is an explicit design assumption, not inferred from steady load.
        thermal=area>=required/(n if model.get('equal_fault_sharing',False) else 1)
        checks={'load_ampacity':current<=amp,'protective_ampacity':current<=protective<=amp,'voltage_drop':abs(drop['percent'])<=limit,'thermal':thermal}
        price=number(cable.get('cost_per_m',0),'cost')*length*n
        econ=model.get('economics',{})
        cost=lifecycle(price,loss,econ.get('hours',4000),econ.get('tariff',.2),econ.get('years',20),econ.get('discount',.05))
        rows.append({'id':cable['id'],'area_mm2':area,'ampacity_a':amp,'drop':drop,'loss_kw':loss,'checks':checks,'feasible':all(checks.values()),'lifecycle_cost':cost,'quantity_m':length*n,'source':cable['source'],'edition':cable['edition']})
    feasible=[r for r in rows if r['feasible']]
    return {'design_current_a':current,'thermal_required_mm2':required,'candidates':rows,'selected':min(feasible,key=lambda r:r['lifecycle_cost'])['id'] if feasible else None,'assumptions':['Catalog ratings and correction factors require project verification.','Equal impedance parallel load sharing.','Adiabatic model; k and clearing duration supplied by user.','Approximate steady-state longitudinal voltage drop.','Protective-device breaking capacity and disconnection time are separate checks.']}

def sensitivity(model,temperatures):
    return [{'temperature_c':t,'result':design(dict(model,temperature_c=t))} for t in temperatures]

def protective_conductor(phase_area,k_phase,k_pe):
    """Conservative adiabatic equivalence; no normative table inferred."""
    return number(phase_area,'phase area',strict=True)*number(k_phase,'phase k',strict=True)/number(k_pe,'PE k',strict=True)
