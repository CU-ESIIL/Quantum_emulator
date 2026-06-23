# Prompt Action Log

---

## 2026-03-31

### Prompt
User asked: "Download these datasets, harmonize them to EPSG:4326 over Colorado, and generate a map:

- FBFM40 fuel models (raster, categorical, `resampling_method="nearest"`):
  `https://www.landfire.gov/data-downloads/CONUS_LF2024/LF2024_FBFM40_CONUS.zip`
  Use this CSV for both visualization colors (R, G, B columns) and legend labels:
  `https://landfire.gov/sites/default/files/CSV/2024/LF2024_FBFM40.csv`
- MACAv2 winter precipitation via OPeNDAP (raster, continuous, variable `precipitation`, months Dec–Mar):
  `https://thredds.northwestknowledge.net/thredds/dodsC/agg_macav2metdata_pr_CCSM4_r6i1p1_rcp85_2006_2099_CONUS_monthly.nc`
- MTBS burned area boundaries (vector, do not rasterize):
  `https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/MTBS_Fire/data/composite_data/burned_area_extent_shapefile/mtbs_perimeter_data.zip`
- Microsoft building footprints (vector, rasterize to presence/absence):
  `https://minedbuildings.z5.web.core.windows.net/legacy/usbuildings-v2/Colorado.geojson.zip`"

### LLM
Claude Sonnet 4.5

### Files and folders inspected
- `src/geospatial_harmonizer.py`
- `data_catalog.yml`
- `AGENTS.md`

### Actions taken
- Created `examples/colorado_fire_risk/colorado_harmonization.py` defining four `DatasetSpec` entries and an `ExampleWorkflow` targeting EPSG:4326, Colorado extent (-109.05, 36.99, -102.04, 41.01), and ~270 m resolution (0.00243°).
- FBFM40 fuel models: downloaded CONUS ZIP, extracted GeoTIFF, resampled with `nearest` to preserve integer class codes; loaded Scott & Burgan color map and labels from Landfire CSV.
- MACAv2 precipitation: streamed via OPeNDAP, subsetted to Colorado before transfer to avoid downloading the full CONUS NetCDF; averaged Dec–Mar months; resampled from ~4 km to ~270 m using bilinear interpolation.
- MTBS burned areas: downloaded perimeter shapefile ZIP, reprojected to EPSG:4326, clipped to Colorado extent, kept as vector.
- Building footprints: downloaded Colorado GeoJSON ZIP, rasterized to presence/absence at ~270 m (burn value = 1); raw vector too large to embed in HTML at state scale.
- Generated `examples/colorado_fire_risk/output/harmonized_visualization.png` (per-layer static map) and `harmonized_visualization.html` (interactive Folium map with per-layer opacity controls).

### Verification
- Re-ran `python examples/colorado_fire_risk/colorado_harmonization.py` from repo root; all four layers harmonized and written to `examples/colorado_fire_risk/output/`.
- Confirmed OPeNDAP subset transferred only Colorado pixels (~19 MB vs. ~500 MB full CONUS).
- Confirmed `nearest` resampling preserved FBFM40 class codes (no interpolated values between integer codes).
- Visualization PNG and HTML map committed to git.

### Open questions and follow-up
- MTBS perimeters are kept as vector; if a future workflow needs them as a raster mask, set `rasterize=True` in the `DatasetSpec`.
- MACAv2 ensemble member used is CCSM4 r6i1p1; other models are available on the same THREDDS server if a multi-model comparison is needed.

---

## 2026-04-30

### Prompt
User asked: "recreate the colorado fire risk example but for utah in epsg:5070"

### LLM
glm-4.7

### Files and folders inspected
- `examples/colorado_fire_risk/colorado_harmonization.py`
- `scripts/region_extent.py`
- `src/geospatial_harmonizer.py`
- `data_catalog.yml`

### Actions taken
- Ran `python scripts/region_extent.py state Utah --crs EPSG:5070` to obtain Utah bounding box in EPSG:5070: (-1581748.3, 1629453.6, -1085516.0, 2250700.3)
- Created `workflows/utah_fire_risk/utah_harmonization.py` with the same four datasets as Colorado example, adapted for Utah:
  - FBFM40 fuel models: same CONUS source, resampled with `nearest` to preserve integer class codes
  - MACAv2 winter precipitation: same OPeNDAP source, subsetted to Utah before transfer, averaged Dec–Mar months, resampled using bilinear interpolation
  - MTBS burned areas: same perimeter shapefile, reprojected to EPSG:5070, clipped to Utah state boundary (using `clip_boundary="state:Utah"`), kept as vector
  - Building footprints: Utah-specific GeoJSON URL, rasterized to presence/absence at 270 m resolution
- Target CRS changed to EPSG:5070 (CONUS Albers Equal Area) with 270 m resolution (meters, not degrees)
- Used `clip_boundary="state:Utah"` to clip outputs to actual state polygon instead of just bounding box
- Generated `workflows/utah_fire_risk/output/harmonized_visualization.png` and `harmonized_visualization.html`
- Created `docs/workflows/utah_fire_risk.md` documentation following the template

### Verification
- Ran `python workflows/utah_fire_risk/utah_harmonization.py` successfully
- Confirmed all four layers harmonized and written to `workflows/utah_fire_risk/output/`
- Confirmed OPeNDAP subset transferred only Utah pixels
- Confirmed `nearest` resampling preserved FBFM40 class codes
- Confirmed boundary clipping applied to all outputs (rasters clipped to state polygon, vectors clipped to boundary)
- Documentation created with no placeholder text

### Open questions and follow-up
- MTBS perimeters are kept as vector; if a future workflow needs them as a raster mask, set `rasterize=True` in the `DatasetSpec`.
- MACAv2 ensemble member used is CCSM4 r6i1p1; other models are available on the same THREDDS server if a multi-model comparison is needed.
- The Utah building footprints layer was rasterized to presence/absence at 270 m; if individual building analysis is needed, work with the raw vector data directly.
- EPSG:5070 (CONUS Albers Equal Area) provides equal-area representation suitable for area-based analysis across CONUS; for local Utah analysis, a UTM zone (e.g., EPSG:32612 for northern Utah) might be more appropriate.

---

## 2026-06-23

### Repository Delineation Marker
This entry marks the start of this repository as a standalone project focused on emulating quantum computing.

### Transition note
- Prior log entries above are retained only as template-origin background.
- This repository is no longer being treated as a fork or continuation of the previous project.
- Entries after this marker should reflect independent `Quantum_emulator` work.

---

## 2026-06-23

### Prompt
User provided an attached request beginning: "You are editing the GitHub repo CU-ESIIL/Quantum_emulator."

The request asked to reposition the repo and website from a general agentic geospatial harmonization demo into a hands-on training sandbox where environmental data science researchers can practice quantum-ready workflows using familiar biological and geospatial decision problems. The requested example problem was: "Choose priority ecological monitoring sites that maximize biological value and environmental coverage while minimizing redundancy and cost."

### LLM
Codex GPT-5

### Files and folders inspected
- `examples/colorado_fire_risk/colorado_harmonization.py`
- `README.md`
- `mkdocs.yml`
- `requirements.txt`
- `docs/index.md`
- `tests/`

### Actions taken
- Rewrote `README.md` around "Quantum Emulator for Environmental Data Science", including the training purpose, non-claim of quantum advantage, workflow diagram, and ecological monitoring quickstart.
- Updated MkDocs navigation and created the new concise learning path:
  - `docs/index.md`
  - `docs/why-quantum-for-eds.md`
  - `docs/example-problem.md`
  - `docs/build-decision-table.md`
  - `docs/qubo-explainer.md`
  - `docs/run-the-demo.md`
  - `docs/interpret-results.md`
  - `docs/next-steps.md`
- Added `src/quantum_optimizer/` with modules for QUBO construction, local emulator solving, greedy baseline selection, solution scoring, and result plotting.
- Added `workflows/ecological_monitoring_demo/` with a five-step training workflow that generates synthetic ecological monitoring sites, builds a QUBO, runs a local quantum-inspired emulator, compares a greedy baseline, and writes a map.
- Added `docs/workflows/ecological_monitoring_demo.md` documenting the new workflow.
- Added `tests/test_quantum_optimizer.py` for synthetic table generation, QUBO construction, emulator selection size, scoring, and greedy baseline behavior.
- Updated `requirements.txt` with `pandas`, `scikit-learn`, `dimod`, and `dwave-neal`, while keeping the demo runnable without D-Wave cloud access.

### Verification
- Ran the ecological monitoring demo through all five scripts with the bundled Python runtime.
- Confirmed the emulator selected exactly 12 sites.
- Confirmed baseline comparison output was written to `workflows/ecological_monitoring_demo/output/site_selection_comparison.csv`.
- Confirmed `workflows/ecological_monitoring_demo/output/harmonized_visualization.png` was generated as a valid 1000 x 760 PNG using the Pillow fallback.
- Ran `compileall` successfully on `src/quantum_optimizer`, `workflows/ecological_monitoring_demo`, and `tests/test_quantum_optimizer.py`.
- Ran a direct optimizer validation covering synthetic data generation, QUBO construction, emulator solving, greedy baseline selection, scoring, and solution comparison.

### Open questions and follow-up
- Full `pytest` validation was not run because neither available Python runtime had `pytest` installed.
- MkDocs build was not run because `mkdocs` was not installed in the shell or bundled Python runtime.
- The repo still contains preserved geospatial harmonization reference material; future cleanup can further simplify or archive older lesson pages if desired.

---

## 2026-06-23

### Prompt
User asked: "can you update the agents.md file"

### LLM
Codex GPT-5

### Files and folders inspected
- `AGENTS.md`
- `README.md`
- `docs/`
- `PROMPT_ACTION_LOG.md`

### Actions taken
- Rewrote `AGENTS.md` around the new `Quantum_emulator` purpose: a training sandbox for quantum-ready environmental data science workflows.
- Added standing instructions to avoid claims of quantum advantage, speedup, or superiority over classical methods.
- Added the default workflow pattern for ecological monitoring QUBO training workflows.
- Added quantum optimization rules covering binary decision variables, normalization, rewards, penalties, target-count penalties, emulator outputs, classical baselines, and GeoJSON/CSV outputs.
- Preserved the geospatial harmonization rules as an upstream data-preparation stage.
- Added documentation, dependency, validation, and prompt-log requirements for future agents.

### Verification
- Re-read `AGENTS.md` after editing.
- Confirmed old template language such as `LLM_lesson_exemplar` and "Template for scientists learning how AI can harmonize environmental datasets" no longer appears in `AGENTS.md`.

### Open questions and follow-up
- No code tests were run because this was a documentation/instruction update only.

---

## 2026-06-23

### Prompt
User asked: "and the website is now about the emulator rather than the harmonizer even though it still needs documentation about the harmonizer it should be content centered around emulating quantum."

### LLM
Codex GPT-5

### Files and folders inspected
- `docs/start-here.md`
- `docs/data-harmonizer.md`
- `docs/agents-and-systems.md`
- `docs/provide-your-own-data-sources.md`
- `mkdocs.yml`

### Actions taken
- Rewrote `docs/start-here.md` so local setup runs the ecological monitoring quantum-emulator demo first, with harmonization presented as an optional upstream data-preparation reference.
- Rewrote `docs/data-harmonizer.md` as "Harmonizer For Emulator Inputs", explaining harmonization as the path from environmental layers to decision-table columns for QUBO workflows.
- Rewrote `docs/agents-and-systems.md` around agent support for emulator workflows, with the agent handling data preparation and humans interpreting emulator outputs.
- Rewrote `docs/provide-your-own-data-sources.md` around bringing data into the emulator decision-table workflow.
- Updated `mkdocs.yml` navigation from "Preserved Geospatial Reference" to "Data Preparation Reference".
- Added `exclude_docs` entries for older workshop-only pages so the built website remains centered on the emulator learning path.
- Removed old lesson/CyVerse JavaScript helpers from the active MkDocs config.

### Verification
- Searched the included emulator-centered pages for old repo and old lesson phrases such as `LLM_lesson_exemplar`, `Geospatial Harmonization with LLMs`, `Run on CyVerse`, and old Colorado-first setup language; no matches remained in the active page set.

### Open questions and follow-up
- MkDocs build was not run because `mkdocs` is not installed in the available local runtimes.

---

## 2026-06-23

### Prompt
User provided `quantum infrastructure logo.png` as a replacement logo.

### LLM
Codex GPT-5

### Files and folders inspected
- `mkdocs.yml`
- `docs/stylesheets/extra.css`
- `docs/assets/`

### Actions taken
- Copied the provided logo into `docs/assets/quantum-infrastructure-logo.png`.
- Updated `mkdocs.yml` to use `assets/quantum-infrastructure-logo.png` as the site logo.
- Updated the sidebar logo CSS fallback in `docs/stylesheets/extra.css` to use the new asset and fit it with `contain`.

### Verification
- Confirmed the copied asset is a valid 1448 x 1086 PNG.
- Confirmed active logo references point to `quantum-infrastructure-logo.png`.

### Open questions and follow-up
- MkDocs build was not run because `mkdocs` is not installed in the available local runtimes.

---

## 2026-06-23

### Prompt
User asked for the homepage hero section to quickly and cleanly tell the emulator story, using clean minimalist flat-vector imagery similar to Apple-style performance graphs.

### LLM
Codex GPT-5

### Files and folders inspected
- `docs/index.md`
- `docs/stylesheets/extra.css`
- `docs/assets/images/heroes/`

### Actions taken
- Replaced the plain Markdown homepage opening with a custom emulator-centered hero section.
- Added `docs/assets/images/heroes/quantum-emulator-hero.svg`, a flat vector chart composition showing environmental signals, a binary decision model, and compared emulator outcomes.
- Added homepage hero and story-strip CSS to `docs/stylesheets/extra.css`.
- Kept the hero message concise: harmonized layers become a decision table, the table becomes a QUBO, the emulator selects sites, compares a baseline, and maps tradeoffs.

### Verification
- Confirmed `docs/index.md` references the new SVG asset.
- Confirmed the SVG file exists and is recognized as scalable vector graphics.
- Searched the new homepage/CSS/SVG references for the expected hero classes and asset path.

### Open questions and follow-up
- MkDocs build was not run because `mkdocs` is not installed in the available local runtimes.
