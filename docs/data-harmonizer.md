# Harmonizer For Emulator Inputs

The website centers the quantum emulator, but the emulator still needs good
inputs. In environmental data science, those inputs often begin as mismatched
geospatial layers: biodiversity observations, climate grids, remote sensing
products, land-cover rasters, field sites, access costs, or planning units.

The harmonizer is the preparation layer that turns those sources into comparable
data. In this repository, its role is to support the move from environmental
synthesis to binary optimization.

```text
raw environmental layers -> harmonized layers -> decision table -> QUBO
```

## Why Harmonization Still Matters

The emulator does not operate directly on raw rasters or shapefiles. It operates
on a decision table where each row is a candidate site or planning unit and each
column describes something relevant to the decision.

Harmonization helps create that table by making datasets comparable:

| Input mismatch | Harmonizer task | Why the emulator cares |
|---|---|---|
| Different coordinate systems | Reproject | Site features must refer to the same locations |
| Different raster resolutions | Resample | Candidate sites need comparable environmental values |
| Different study boundaries | Clip | The decision problem needs a shared study area |
| Vector and raster formats | Convert or summarize | Site rows need consistent feature columns |
| Different ecological meanings | Document and derive variables | QUBO rewards and penalties must be interpretable |

## From Layers To Decision Columns

A monitoring-site table might include:

* `species_richness`
* `climate_refugia_score`
* `habitat_connectivity`
* `cost`
* `mean_temp`
* `annual_precip`
* `elevation`
* `region`
* `lat`
* `lon`

Those columns can come from field observations, raster extraction, vector
overlays, or summaries of geospatial data cubes. Once they are in a clean table,
the optimizer can normalize them and build a QUBO.

## Preserved Harmonizer Example

The Colorado fire-risk example remains in the repository as a reference for
AI-assisted geospatial preparation:

```bash
python3 examples/colorado_fire_risk/colorado_harmonization.py
```

It shows how datasets can be downloaded, reprojected, clipped, resampled, and
visualized. In the quantum-emulator storyline, that work is not the endpoint. It
is what prepares environmental layers for a later data-to-decision workflow.

## Scientific Caution

Harmonization choices are scientific choices. Resampling, aggregation,
normalization, and clipping affect what the later optimization problem means.

Before building a QUBO, check:

* whether the variables are comparable
* whether categorical data used nearest-neighbor resampling
* whether continuous data used an appropriate interpolation method
* whether the study boundary matches the decision question
* whether cost and biological value are measured or estimated consistently

The emulator can only explore the decision space it is given. Good harmonization
is how that space becomes meaningful.
