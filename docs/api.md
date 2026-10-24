# API and interchange

```python
from cableroute.cli import load_case
from cableroute.studies import run
model = load_case("example:industrial")
result = run(model, "analyze")
```

Use the public functions in `cableroute.engine` for individual calculations. JSON example fields document the native format. Unknown field names are not interpreted as engineering instructions. HTTP `POST /api/study` accepts `{"network": model, "action": "analyze", "options": {}}`. The historical `network` envelope key contains the entire study model. Requests are limited to 2 MB and same-origin browsers. `GET /api/examples` lists packaged examples. `/api/import` accepts `{"text": "JSON model"}` for validation. CLI `--options` accepts JSON; `--output` writes the full result.

Neutral study options: {"harmonics":[{"order":3,"phases":[[10,0],[10,0],[10,0]]}]}. Protective study options: {"phase_area":50,"k_phase":115,"k_pe":143}. Sensitivity options: {"temperatures":[20,60,90]}. Use harmonic_neutral and parallel_share directly for conductor phasor studies. Catalog prices are monetary units per route metre; quantity is route length times parallel runs, not individual core length.
