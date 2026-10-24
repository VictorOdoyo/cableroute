# demand 04

Input power 40 kW, voltage 400 V, 3 phase, PF 0.82, efficiency 0.89, demand 0.7. Convert kW to watts and divide demanded input power by voltage and PF; three-phase line current includes sqrt(3).

Expected values are recorded in [the reference fixture](../../references/demand_04.json). The executable regression uses relative tolerance 1e-8 and absolute tolerance 1e-8 unless a tighter residual is specified. Values are analytical examples, not standard ampacity or compliance limits.
