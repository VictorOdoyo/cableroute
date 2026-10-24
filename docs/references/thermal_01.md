# thermal 01

Fault 1000 A for 0.05 s with user k=105. Integrate constant I squared over time, then solve S²=I²t/k². No protective-device clearing-time inference.

Expected values are recorded in [the reference fixture](../../references/thermal_01.json). The executable regression uses relative tolerance 1e-8 and absolute tolerance 1e-8 unless a tighter residual is specified. Values are analytical examples, not standard ampacity or compliance limits.
