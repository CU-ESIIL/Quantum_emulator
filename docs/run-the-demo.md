# Run the Quantum Emulator

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Run the full ecological monitoring demo from the repository root:

```bash
python3 workflows/ecological_monitoring_demo/01_make_synthetic_site_table.py
python3 workflows/ecological_monitoring_demo/02_build_qubo.py
python3 workflows/ecological_monitoring_demo/03_run_quantum_emulator.py
python3 workflows/ecological_monitoring_demo/04_compare_baselines.py
python3 workflows/ecological_monitoring_demo/05_map_results.py
```

The default solver runs locally. If `dwave-neal` is installed, the demo uses
local simulated annealing. If it is not installed, the demo falls back to a
small randomized local-search emulator. Neither path requires a D-Wave cloud
account.

## Outputs

Look in `workflows/ecological_monitoring_demo/output/` for:

* `candidate_sites.csv`
* `qubo_summary.json`
* `selected_sites_quantum_emulator.csv`
* `selected_sites_quantum_emulator.geojson`
* `selected_sites_greedy_baseline.csv`
* `site_selection_comparison.csv`
* `harmonized_visualization.png`
