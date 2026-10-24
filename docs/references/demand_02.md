# demand 02

Input power 20 kW, voltage 400 V, 3 phase, PF 0.76, efficiency 0.87, demand 0.6. Convert kW to watts and divide demanded input power by voltage and PF; three-phase line current includes sqrt(3).

Expected values are recorded in [the reference fixture](../../references/demand_02.json). The executable regression uses relative tolerance 1e-8 and absolute tolerance 1e-8 unless a tighter residual is specified. Values are analytical examples, not standard ampacity or compliance limits.
