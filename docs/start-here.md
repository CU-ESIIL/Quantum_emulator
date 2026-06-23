# Local Setup

This page helps you run the quantum-emulator training workflow on your own
computer. The default path uses synthetic ecological monitoring data, builds a
QUBO-style site-selection model, runs a local quantum-inspired emulator, compares
the result with a greedy baseline, and writes outputs you can inspect.

The geospatial harmonizer is still part of the repository, but it now serves as
the data-preparation layer: use it when you need harmonized environmental layers
before building a decision table.

## What You Will Run

The main local workflow is:

```text
candidate sites -> QUBO -> local emulator -> baseline comparison -> map
```

You will:

1. Clone `CU-ESIIL/Quantum_emulator`.
2. Create a local Python environment.
3. Install dependencies.
4. Run the ecological monitoring demo.
5. Inspect selected sites, comparison metrics, and the map output.
6. Optionally run the preserved geospatial harmonizer examples.

No quantum hardware or D-Wave cloud account is required.

## Before You Begin

Make sure you have:

* Git installed.
* Python 3 available from your terminal.
* Permission to install Python packages.
* Enough disk space for generated outputs and optional geospatial downloads.

Check Git and Python:

```bash
git --version
python3 --version
```

## Step 1: Clone The Repository

```bash
git clone https://github.com/CU-ESIIL/Quantum_emulator.git
cd Quantum_emulator
```

Confirm that you are in the repository:

```bash
ls
```

You should see `README.md`, `requirements.txt`, `docs/`, `src/`, `tests/`, and
`workflows/`.

## Step 2: Create A Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Step 3: Install Dependencies

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

The demo can fall back to a local randomized search if `dwave-neal` is not
available. The default workflow does not need a D-Wave cloud account.

## Step 4: Run The Emulator Demo

Run these commands from the repository root:

```bash
python3 workflows/ecological_monitoring_demo/01_make_synthetic_site_table.py
python3 workflows/ecological_monitoring_demo/02_build_qubo.py
python3 workflows/ecological_monitoring_demo/03_run_quantum_emulator.py
python3 workflows/ecological_monitoring_demo/04_compare_baselines.py
python3 workflows/ecological_monitoring_demo/05_map_results.py
```

## Step 5: Inspect Outputs

Outputs are written to:

```text
workflows/ecological_monitoring_demo/output/
```

Look for:

* `candidate_sites.csv`
* `qubo_summary.json`
* `selected_sites_quantum_emulator.csv`
* `selected_sites_quantum_emulator.geojson`
* `selected_sites_greedy_baseline.csv`
* `site_selection_comparison.csv`
* `harmonized_visualization.png`

The comparison table is the main scientific checkpoint. Use it to compare the
emulator and greedy baseline in terms of biological value, cost, environmental
spread, and regions represented.

## Optional: Run The Harmonizer

If you want to see how geospatial data can be prepared before optimization, run
the preserved Colorado harmonization example:

```bash
python3 examples/colorado_fire_risk/colorado_harmonization.py
```

That example is not the center of the site anymore. It is a reference for the
upstream step: turning heterogeneous environmental layers into analysis-ready
inputs for later data-to-decision workflows.

## Common Issues

### Python Is Not Found

Try:

```bash
python --version
```

If `python` works but `python3` does not, use `python` in the commands above.

### A Package Is Missing

Confirm that your virtual environment is active:

```bash
which python3
python3 -m pip list
```

Then reinstall dependencies:

```bash
python3 -m pip install -r requirements.txt
```

### The Map Step Skips Plotting

The plotting helper uses `matplotlib` when available and falls back to `Pillow`
for a simple PNG. If neither package is installed, install the requirements
again.

## Where To Go Next

Continue with [The Example Problem](example-problem.md), then read the
[QUBO / Ising Explainer](qubo-explainer.md) before adapting the workflow to your
own data.
