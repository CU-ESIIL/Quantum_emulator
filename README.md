# Quantum Emulator for Environmental Data Science

This repository is a hands-on training sandbox for environmental data scientists
who want to practice quantum-ready workflows without needing a quantum computer
or a physics background.

The project starts from familiar environmental data science work: harmonizing
geospatial layers, building a biological decision table, and choosing ecological
monitoring sites. It then shows how that decision can be translated into a
binary optimization problem, solved with a local quantum-inspired emulator,
compared with a classical baseline, and mapped back onto geospatial data.

The core idea:

> AI agents can help harmonize and prepare environmental data. Quantum-inspired
> optimization can then help explore decision spaces.

## What This Repo Teaches

* How harmonized environmental layers can become a site-level decision table.
* What a binary decision variable means in a monitoring-site selection problem.
* How to express biological value, environmental coverage, redundancy, cost,
  and a target number of sites as a QUBO-style model.
* How to run a local quantum-inspired emulator on classical hardware.
* How to compare an emulator result with a simple greedy classical baseline.
* How to inspect selected sites as CSV, GeoJSON, and a map.

## What This Repo Does Not Claim

This repository does not demonstrate quantum advantage, speedup, or superior
performance over classical methods. The default workflow runs locally on
classical hardware. The goal is practice: learning how environmental decision
problems can be prepared in forms that are compatible with quantum-inspired,
quantum-emulated, and eventually quantum or hybrid optimization tools.

No D-Wave cloud account is required for the default demo.

## Workflow

```text
harmonized environmental layers
        |
        v
biological decision table
        |
        v
site-selection objective
        |
        v
QUBO / Ising-style binary optimization model
        |
        v
local quantum-inspired emulator
        |
        v
classical greedy baseline comparison
        |
        v
selected sites mapped back to geography
```

Example problem:

> Choose priority ecological monitoring sites that maximize biological value
> and environmental coverage while minimizing redundancy and cost.

## Quickstart

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the ecological monitoring demo:

```bash
python3 workflows/ecological_monitoring_demo/01_make_synthetic_site_table.py
python3 workflows/ecological_monitoring_demo/02_build_qubo.py
python3 workflows/ecological_monitoring_demo/03_run_quantum_emulator.py
python3 workflows/ecological_monitoring_demo/04_compare_baselines.py
python3 workflows/ecological_monitoring_demo/05_map_results.py
```

Key outputs are written to `workflows/ecological_monitoring_demo/output/`:

* `candidate_sites.csv`
* `selected_sites_quantum_emulator.csv`
* `selected_sites_quantum_emulator.geojson`
* `selected_sites_greedy_baseline.csv`
* `site_selection_comparison.csv`
* `harmonized_visualization.png`

The demo generates a synthetic but biologically plausible candidate-site table
if no external data are present. In a real ESIIL working group project, this
table could be derived from harmonized rasters, vectors, field observations, or
geospatial data cubes.

## Existing Geospatial Examples

The original geospatial harmonization examples are preserved. They remain useful
for learning how an AI-assisted repository can turn environmental datasets into
aligned analysis-ready layers:

```bash
python3 examples/colorado_fire_risk/colorado_harmonization.py
```

Those examples are now framed as the upstream data-preparation stage for the
quantum-ready optimization workflow.

## Repository Structure

```text
src/
  geospatial_harmonizer.py        # existing geospatial harmonization tools
  quantum_optimizer/              # QUBO, emulator, scoring, and plotting helpers

examples/
  colorado_fire_risk/             # preserved harmonization reference example

workflows/
  ecological_monitoring_demo/     # main quantum-ready training workflow
  utah_fire_risk/                 # preserved harmonization workflow

docs/                             # MkDocs website source
tests/                            # lightweight tests for harmonization and optimizer code
AGENTS.md                         # agent workflow instructions
requirements.txt
```

## Documentation Website

Preview the documentation locally:

```bash
pip install mkdocs mkdocs-material
mkdocs serve
```

Then open `http://127.0.0.1:8000`.

## Notes for Learners

You do not need to start with quantum hardware. Start with emulation on
classical hardware, inspect the decision table, understand the binary variables,
and compare the emulator output with a baseline you can explain. That is the
useful first step toward quantum-ready environmental data science.
