# Bring Your Own Data

The default demo uses synthetic ecological monitoring sites so the emulator
workflow is easy to run. For a real ESIIL working group, the next step is to
replace that synthetic table with variables from your own study system.

The goal is not only to download data. The goal is to produce a decision table
that can feed the QUBO workflow.

```text
your data sources -> harmonized features -> candidate-site table -> emulator
```

## What The Emulator Needs

At minimum, prepare a table where each row is a candidate site, planning unit, or
management option.

Useful columns include:

* `site_id`
* `lat`
* `lon`
* biological value, such as `species_richness`
* climate or resilience value, such as `climate_refugia_score`
* connectivity or complementarity value, such as `habitat_connectivity`
* `cost`
* `region`
* optional environmental features, such as temperature, precipitation, or elevation

The optimizer can work with synthetic data, CSV files, or tables generated from
harmonized rasters and vectors.

## When You Need Direct Download URLs

If your data are geospatial files that need harmonization first, give the agent
direct download URLs rather than landing pages. A direct URL points to the file
itself, such as a `.zip`, `.tif`, `.geojson`, or NetCDF endpoint.

Portal pages are useful for humans, but they often return HTML instead of data.
The harmonizer needs the downloadable file.

## Example Request

Use a request like this when you already know the data sources:

```text
Use these direct data URLs to prepare candidate ecological monitoring sites for
the quantum-emulator workflow. Harmonize the layers over my study area, extract
site-level variables, build a decision table, then run the local emulator and
compare it with the greedy baseline.
```

Include:

* study area or boundary
* direct data URLs
* which variables should become biological rewards
* which variables should become environmental coverage features
* which variables represent cost
* how many sites or planning units should be selected

## Getting A Direct URL From A Portal

Some portals, such as USGS ScienceBase, require a few clicks before the direct
file URL appears.

General pattern:

1. Open the dataset landing page.
2. Find the attached file or download section.
3. Start the file download.
4. Open your browser download history.
5. Copy the actual file URL from the downloaded item.
6. Give that direct URL to the workflow.

Some direct URLs expire. If a workflow later fails with a download error, return
to the portal and copy a fresh URL.

## Use The Harmonizer As Needed

If your candidate table already exists, you can skip geospatial harmonization
and start with the QUBO workflow.

If your variables live in separate spatial layers, use the harmonizer first. The
harmonizer is still documented because it is how many environmental projects
move from raw data into the structured table that the emulator can understand.
