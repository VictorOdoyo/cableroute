# drop 01

Route 25 m, current 20 A, R 0.3 ohm/km, X 0.07, PF 0.6900000000000001, phases 1, leading=False. Resolve impedance along the voltage axis, apply route length and phase multiplier. Leading reactance subtracts.

Expected values are recorded in [the reference fixture](../../references/drop_01.json). The executable regression uses relative tolerance 1e-8 and absolute tolerance 1e-8 unless a tighter residual is specified. Values are analytical examples, not standard ampacity or compliance limits.
