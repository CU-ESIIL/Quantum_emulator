# Ecological Monitoring Demo

This workflow shows how a familiar environmental decision problem can be
translated into a small binary optimization exercise.

Problem:

> Choose 12 ecological monitoring sites from 100 candidates, maximizing
> biological value and environmental coverage while minimizing redundancy and
> cost.

The demo uses synthetic but biologically plausible site data by default. That
keeps the workflow lightweight and runnable without external downloads. In a
real working group project, the same table could come from harmonized rasters,
vectors, field observations, or a geospatial data cube.

## Run

From the repository root:

```bash
python3 workflows/ecological_monitoring_demo/01_make_synthetic_site_table.py
python3 workflows/ecological_monitoring_demo/02_build_qubo.py
python3 workflows/ecological_monitoring_demo/03_run_quantum_emulator.py
python3 workflows/ecological_monitoring_demo/04_compare_baselines.py
python3 workflows/ecological_monitoring_demo/05_map_results.py
```

Outputs are written to `workflows/ecological_monitoring_demo/output/`.

This is a quantum-ready training example, not a demonstration of quantum
advantage. The default solver runs locally on classical hardware.
