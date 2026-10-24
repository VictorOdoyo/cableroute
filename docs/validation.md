# Validation record

Validated on 2026-10-24 with Python 3.13.15 and NumPy 2.1.2 on Windows. All 91 unit/integration tests pass. Seventy closed-form reference cases cover ten calculation families; every case has its own recorded inputs, expected values and derivation. HTTP tests exercise real loopback requests, packaged assets and origin rejection. GitHub CI also validates Python 3.11, 3.12 and 3.13 on Ubuntu.

Browser checks: industrial example calculation, study switching, specialized result values, current study labels and charts. Additional checks exercised JSON error feedback and stale-export disabling. CableRoute temperature sensitivity and harmonic neutral examples were run; HarmonicLens frequency scan, load flow and filter design were run. Screenshots show a real running model and are included in this repository.

The examples are analytical and illustrative. No field installation, manufacturer certification, IEC/IEEE compliance test suite or calibrated measurement instrument is represented by this record. See engineering scope in README for model limits.
