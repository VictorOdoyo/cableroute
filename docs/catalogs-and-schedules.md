# Catalogs, neutral policy and feeder schedules

`cableroute.catalog.import_csv(text)` requires id, area_mm2, ampacity_a, r20_ohm_km, x_ohm_km, source, edition, installation and material. Optional cost_per_m and alpha retain the same meaning as JSON. Numeric values are parsed explicitly and duplicate IDs are rejected. Supply the actual manufacturer/standard source and edition rather than relabeling demo ratings.

`neutral_selection(harmonics, candidates, factors, minimum_area_mm2, fault)` combines phasor neutral RMS, derated candidate ampacity, an explicit policy minimum and optional adiabatic area. Fault is a dictionary with current_a, seconds and k. Minimum area policy must be set by the engineer for the installation and earthing system.

`feeder_schedule([{"id":"F1","model":model}])` returns selected sizes, route quantities, loss and lifecycle cost. `schedule_csv(rows)` writes a spreadsheet-safe CSV. Infeasible feeders retain null selections and quantities rather than silently omitting the feeder. `installation_sensitivity(model, {"case": factors})` compares complete factor scenarios. These Python APIs complement the workbench temperature study.
