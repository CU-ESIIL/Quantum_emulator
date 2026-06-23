# Ecological Monitoring Demo

## Prompt

User asked for the repository to be repositioned as a hands-on training sandbox
where environmental data science researchers can practice quantum-ready
workflows using familiar biological and geospatial decision problems.

## Datasets

This workflow uses a synthetic ecological monitoring candidate-site table by
default. The generated table includes:

* `site_id`
* `lat`
* `lon`
* `species_richness`
* `climate_refugia_score`
* `habitat_connectivity`
* `cost`
* `region`
* `mean_temp`
* `annual_precip`
* `elevation`

The synthetic table is a teaching stand-in for a real table produced from
harmonized environmental layers, geospatial data cubes, field observations, or
working-group datasets.

## Method

The workflow selects 12 monitoring sites from 100 candidates. It builds a
QUBO-style binary optimization model where each variable represents whether a
site is selected. The model rewards biological value and environmental coverage,
then penalizes cost, redundancy, and missing the requested number of selected
sites.

The default solver runs locally. It uses `dwave-neal` simulated annealing when
available and falls back to a small randomized local-search emulator otherwise.
No D-Wave cloud account is required.

## Result

The workflow writes selected sites from the quantum-inspired emulator and a
greedy classical baseline, plus a comparison table and map:

* `selected_sites_quantum_emulator.csv`
* `selected_sites_quantum_emulator.geojson`
* `selected_sites_greedy_baseline.csv`
* `selected_sites_greedy_baseline.geojson`
* `site_selection_comparison.csv`
* `harmonized_visualization.png`

This result is for practice and interpretation. It does not claim quantum
advantage.
