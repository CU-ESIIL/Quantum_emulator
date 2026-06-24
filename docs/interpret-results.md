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

This is the right interpretation. The result is not "the emulator won" or "the
baseline won." It is "these two methods expose different decision priorities."
That is often more valuable for EDS than a single winner, because environmental
planning is shaped by stakeholder priorities, field logistics, uncertainty, and
ecological judgment.

Useful columns include:

* `n_sites`: how many sites were selected
* `mean_biological_value`: average normalized biological value
* `total_cost`: total implementation cost for the selected network
* `mean_environmental_distance`: how spread out the selected sites are in
  environmental feature space
* `regions_represented`: how many named regions appear in the selection

## Reading The Current Result

| Question | What the checked-in demo suggests |
|---|---|
| Did both methods satisfy the target count? | Yes, both selected 12 sites. |
| Which method favored biological value? | The greedy baseline had higher mean biological value. |
| Which method favored environmental spread? | The emulator had higher mean environmental distance. |
| Which method was cheaper in this run? | The greedy baseline had lower total cost. |
| Did either method cover more named regions? | No, both represented 3 regions. |

For a real working group, this table is the start of interpretation, not the end
of it. The next step is to inspect which sites changed and whether those changes
make ecological, logistical, and governance sense.

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

## What Would Make The Evidence Stronger?

A stronger analysis would run a scenario ensemble:

* vary objective weights across plausible ranges
* repeat stochastic solvers with multiple random seeds
* compare against stronger classical baselines
* summarize how often each site is selected
* map sites that are stable across scenarios
* document which ecological assumptions drive each solution

That is the direction this training workflow points toward.
