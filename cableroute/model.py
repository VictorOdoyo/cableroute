import json
from .engine import design
def validate(model):
    copy=json.loads(json.dumps(model,allow_nan=False));design(copy);return copy
