# drop 02

Route 50 m, current 40 A, R 0.15 ohm/km, X 0.07, PF 0.73, phases 3, leading=False. Resolve impedance along the voltage axis, apply route length and phase multiplier. Leading reactance subtracts.

Expected values are recorded in [the reference fixture](../../references/drop_02.json). The executable regression uses relative tolerance 1e-8 and absolute tolerance 1e-8 unless a tighter residual is specified. Values are analytical examples, not standard ampacity or compliance limits.
