# Build a Decision Table

The decision table is the bridge between harmonized environmental data and
optimization.

Each row is a candidate site. Each column describes something relevant to the
decision: biological value, environmental setting, cost, region, or geometry.

This table is the methods section in miniature. It records what the decision
model is allowed to know. If an ecological value, cost, access constraint, or
region label is missing from the table, the optimizer cannot account for it.

```text
site_id | lat | lon | species_richness | climate_refugia_score | cost | region
S001    | ... | ... | 67.2             | 0.81                  | 5100 | montane
```

## From Layers To Rows

In a real project, the table might come from:

* extracting raster values at candidate monitoring locations
* summarizing geospatial data cubes by planning unit
* joining field observations to habitat layers
* adding travel or implementation cost estimates

The synthetic demo starts at this table so learners can focus on the
optimization idea before connecting external data.

For real projects, this is where analysis-ready geospatial work matters.
Platforms such as the [Open Data Cube](https://www.opendatacube.org/) emphasize
organized, analysis-ready Earth observation data because decision workflows need
consistent spatial and temporal inputs before modeling begins.

## Normalization

The optimizer normalizes biological value, cost, and environmental feature
columns onto 0-1 scales. This keeps variables with large units, such as
elevation or cost, from dominating the model only because of their units.

Normalization is not just a software convenience. It is a modeling decision.
After normalization, weights such as `value_weight`, `coverage_weight`, and
`cost_weight` express relative priority rather than accidental differences in
measurement units.

## Minimum Viable Decision Table

A useful first table should include:

* a unique `site_id`
* a binary-selectable row for each candidate site or planning unit
* at least one biological value column
* at least one environmental feature column for coverage or complementarity
* a cost column
* `lat` and `lon` if results should be mapped
* provenance notes describing where each column came from

The better the table, the more meaningful the emulator experiment.
