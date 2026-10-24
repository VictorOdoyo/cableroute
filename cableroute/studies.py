import hashlib,json
from .model import validate
from .engine import design,sensitivity,harmonic_neutral,protective_conductor
def run(model,action='analyze',options=None):
    model=validate(model);options=options or {}
    if action=='analyze':result=design(model)
    elif action=='sensitivity':result={'temperatures':sensitivity(model,options.get('temperatures',[20,40,60,70,90]))}
    elif action=='neutral':result={'neutral_rms_a':harmonic_neutral(options['harmonics'])}
    elif action=='protective':result={'required_mm2':protective_conductor(**options)}
    else:raise ValueError('Unknown study')
    result['provenance']={'model_sha256':hashlib.sha256(json.dumps(model,sort_keys=True).encode()).hexdigest(),'action':action,'options':options,'version':'1.0.0'}
    return result
