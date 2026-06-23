# Interpret the Results

The emulator output is a selected set of monitoring sites. The comparison table
helps interpret that set against a simple greedy classical baseline.

Useful columns include:

* `n_sites`: how many sites were selected
* `mean_biological_value`: average normalized biological value
* `total_cost`: total implementation cost for the selected network
* `mean_environmental_distance`: how spread out the selected sites are in
  environmental feature space
* `regions_represented`: how many named regions appear in the selection

## What To Look For

The emulator and greedy baseline may choose different sites. That is expected.
The point is not that one is automatically better. The point is to inspect the
tradeoffs: biological value, cost, redundancy, and environmental coverage.

For working groups, this step is where scientific judgment returns to the
center. The solver proposes a decision; researchers evaluate whether the
decision makes ecological and logistical sense.
