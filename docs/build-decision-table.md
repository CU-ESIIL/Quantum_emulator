# Build a Decision Table

The decision table is the bridge between harmonized environmental data and
optimization.

Each row is a candidate site. Each column describes something relevant to the
decision: biological value, environmental setting, cost, region, or geometry.

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

## Normalization

The optimizer normalizes biological value, cost, and environmental feature
columns onto 0-1 scales. This keeps variables with large units, such as
elevation or cost, from dominating the model only because of their units.
