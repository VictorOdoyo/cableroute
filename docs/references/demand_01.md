# demand 01

Input power 10 kW, voltage 230 V, 1 phase, PF 0.73, efficiency 0.86, demand 0.55. Convert kW to watts and divide demanded input power by voltage and PF; three-phase line current includes sqrt(3).

Expected values are recorded in [the reference fixture](../../references/demand_01.json). The executable regression uses relative tolerance 1e-8 and absolute tolerance 1e-8 unless a tighter residual is specified. Values are analytical examples, not standard ampacity or compliance limits.
