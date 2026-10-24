# Engineering conventions

Power is mechanical/output kW when efficiency is below one; divide by efficiency to obtain input power. Three-phase voltage is line-to-line. Length is one-way route metres, resistance/reactance per conductor in ohm/km. Areas are mm². Drop is longitudinal, not an exact receiving-voltage solution. Loss is conductor I²R in kW. Factors multiply base ampacity; they do not replace installation-table selection. Feasibility requires every returned check to pass; no feasible selection is reported as null. Economic ranking is only among feasible entries, using end-year loss costs and explicit discount rate.

Every report carries its model hash, options, action and software version. The hash identifies input equality, not professional certification. All floating-point values must be finite. Recalculate after any input change. Engineering review remains project-specific.
