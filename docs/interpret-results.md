# Interpret the Results

The emulator output is a selected set of monitoring sites. The comparison table
helps interpret that set against a simple greedy classical baseline.

The current checked-in demo shows a useful tradeoff. The emulator selected the
same number of sites as the greedy baseline, but produced a network with higher
mean environmental distance. In plain language, it spread the selected sites
farther across environmental feature space. The greedy baseline had higher mean
biological value and lower total cost.

That does not make either method automatically better. It shows what the
workflow is for: comparing decision tradeoffs in a way environmental scientists
can inspect.

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

## Why This Is Useful For EDS

Environmental data science often supports decisions with competing goals. A
monitoring network may need to be biologically rich, environmentally broad,
affordable, accessible, and defensible to collaborators.

The emulator workflow helps by making those priorities explicit. Instead of
arguing about an opaque score, a working group can adjust weights, rerun the
experiment, and see which sites move in or out of the solution. The result is a
clearer data-to-decision conversation.
