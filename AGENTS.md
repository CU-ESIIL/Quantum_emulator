# AGENTS.md

## Repository Purpose

This repository is a training sandbox for environmental data scientists,
ecologists, geospatial analysts, and ESIIL working groups learning
quantum-ready environmental workflows.

Core narrative:

> AI agents can help harmonize and prepare environmental data. Quantum-inspired
> optimization can then help explore decision spaces.

The main learning path is:

1. Harmonize environmental or geospatial layers.
2. Convert harmonized layers into a biological decision table.
3. Define a site-selection problem.
4. Build a QUBO / Ising-style binary optimization formulation.
5. Solve it locally with a quantum-inspired emulator.
6. Compare against a simple classical baseline.
7. Map and explain the selected sites.

Do not claim quantum advantage, quantum speedup, or superiority over classical
methods. Frame this repo honestly as practice with quantum-inspired and
quantum-ready methods on classical hardware.

---

## First Files To Read

Before changing code, inspect the relevant reference workflow:

- Quantum-ready optimization workflow:
  `workflows/ecological_monitoring_demo/README.md`
- Optimizer source:
  `src/quantum_optimizer/build_qubo.py`
  `src/quantum_optimizer/solve_emulator.py`
  `src/quantum_optimizer/classical_baseline.py`
  `src/quantum_optimizer/score_solution.py`
  `src/quantum_optimizer/plot_results.py`
- Preserved geospatial harmonization example:
  `examples/colorado_fire_risk/colorado_harmonization.py`
- Website narrative:
  `README.md`
  `docs/index.md`
  `docs/qubo-explainer.md`
  `docs/run-the-demo.md`

Use the existing style and workflow structure before adding new abstractions.

---

## Default Workflow Pattern

For new training workflows, create a folder under:

```text
workflows/<project_name>/
```

Use clear numbered scripts when the workflow is instructional:

```text
01_prepare_or_make_site_table.py
02_build_qubo.py
03_run_quantum_emulator.py
04_compare_baselines.py
05_map_results.py
output/
```

Always set output paths relative to the workflow script:

```python
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
```

Keep the default path runnable locally. Do not require a D-Wave cloud account,
API token, remote solver, or external service for the standard demo.

---

## Required Script Header

Every workflow script that imports from `src/` must include this bootstrap
header before importing repository modules:

```python
import sys
from pathlib import Path

_repo_root = next(p for p in Path(__file__).resolve().parents
                  if (p / "src" / "geospatial_harmonizer.py").exists())
sys.path.insert(0, str(_repo_root))
```

Then import the needed package:

```python
from src.quantum_optimizer import build_site_selection_qubo, solve_site_selection
```

For geospatial harmonization workflows, import:

```python
from src.geospatial_harmonizer import (
    DatasetSpec,
    ExampleWorkflow,
    run_harmonization_example,
)
```

---

## Quantum Optimization Rules

When building or editing QUBO workflows:

- Explain that a binary decision variable means `1 = select this site` and
  `0 = do not select this site`.
- Normalize biological value, climate score, cost, and environmental feature
  columns before combining them.
- Model biological value as a reward.
- Model environmental coverage as a reward or diversity objective.
- Model redundancy between similar selected sites as a pairwise penalty.
- Model cost as a penalty.
- Include a target-count penalty when the user asks for a fixed or approximate
  number of selected sites.
- Compare emulator output with a transparent classical baseline.
- Output selected sites as CSV, and GeoJSON when `lat` and `lon` are available.
- Keep comments educational but concise.

Default example problem:

> Choose priority ecological monitoring sites that maximize biological value and
> environmental coverage while minimizing redundancy and cost.

Preferred outputs:

```text
candidate_sites.csv
candidate_sites_normalized.csv
qubo_summary.json
quantum_emulator_solution.json
selected_sites_quantum_emulator.csv
selected_sites_quantum_emulator.geojson
selected_sites_greedy_baseline.csv
selected_sites_greedy_baseline.geojson
site_selection_comparison.csv
harmonized_visualization.png
```

The static visualization filename should remain exactly
`harmonized_visualization.png` so the documentation hook can find it.

---

## Geospatial Harmonization Rules

The original geospatial harmonization examples are preserved as the upstream
data-preparation stage. Do not break them.

When adding or editing geospatial harmonization workflows:

1. Validate direct download URLs:
   ```bash
   python3 scripts/check_urls.py <url1> <url2> ...
   ```
   Stop if any fail.
2. Search the data catalog when the user asks by topic:
   ```bash
   python3 scripts/find_dataset.py <keyword>
   ```
3. Get region bounds for US states, counties, or places:
   ```bash
   python3 scripts/region_extent.py state Colorado
   python3 scripts/region_extent.py county Larimer Colorado --crs EPSG:5070
   python3 scripts/region_extent.py place Boulder CO
   ```
4. Always set `clip_boundary` on `ExampleWorkflow` when a state, county, or
   place boundary is known, for example `clip_boundary="state:Colorado"`.
5. Set `output_dir=Path(__file__).parent / "output"`.

For non-US regions, ask the user for a boundary file or bounding box.

Resampling rules:

- Categorical data such as land cover or fuel models:
  `resampling_method="nearest"`
- Continuous data such as temperature or precipitation:
  `resampling_method="bilinear"`
- If unsure, ask the user.

Failure handling:

- Download fails: stop and tell the user which URL failed.
- URL returns HTML: tell the user it is a portal link and ask for a direct
  download URL.
- No valid geospatial files found: stop and ask the user.

GDAL CLI tools such as `gdalwarp`, `ogr2ogr`, and `gdal_translate` may be used
for format conversion or preprocessing before running the harmonizer.

---

## Documentation Requirements

For any new user-facing workflow:

1. Add or update a workflow README in `workflows/<project_name>/README.md`.
2. Add a documentation page at `docs/workflows/<project_name>.md`.
3. Include these sections in workflow docs:
   - `## Prompt`
   - `## Datasets`
   - `## Result`
4. Keep the tone practical, plain-language, and scientific.
5. Use ESIIL-style framing when appropriate:
   - data-to-decision
   - environmental synthesis
   - geospatial data cubes
   - biological monitoring
   - working groups

Preserve the agentic AI connection, but recast it as data preparation and
workflow support rather than the whole purpose of the repository.

---

## Dependency Rules

Use `pandas`, `numpy`, `scikit-learn`, and `matplotlib` when they are useful for
the teaching workflow.

`dimod` and `dwave-neal` are allowed, but must remain optional at runtime:

- If `dwave-neal` is installed, local simulated annealing may be used.
- If it is missing, fall back gracefully to local randomized or greedy search.
- Do not add a required D-Wave cloud dependency to the default path.

---

## Validation Checklist

After editing code or docs, run what is available in the environment:

```bash
python3 workflows/ecological_monitoring_demo/01_make_synthetic_site_table.py
python3 workflows/ecological_monitoring_demo/02_build_qubo.py
python3 workflows/ecological_monitoring_demo/03_run_quantum_emulator.py
python3 workflows/ecological_monitoring_demo/04_compare_baselines.py
python3 workflows/ecological_monitoring_demo/05_map_results.py
```

Run tests when dependencies are installed:

```bash
python3 -m pytest
```

Build docs when MkDocs is installed:

```bash
mkdocs build --strict
```

If validation cannot run because a dependency is missing, say exactly what was
missing and what was still verified.

---

## Prompt Action Log

After substantial work, append to `PROMPT_ACTION_LOG.md`:

- date
- user's exact prompt or a faithful quoted summary
- model name
- files and folders inspected
- actions taken
- verification performed
- open questions or follow-up

This log is part of the scientific record for the agentic repository. Keep it
concise but specific.
