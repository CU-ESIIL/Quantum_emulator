# The Example Problem

The training problem is:

> Choose priority ecological monitoring sites that maximize biological value
> and environmental coverage while minimizing redundancy and cost.

This is intentionally familiar. Environmental data scientists and ecologists
already make decisions like this when designing monitoring networks, prioritizing
field campaigns, or choosing conservation areas.

## Candidate Sites

The demo creates 100 synthetic candidate sites. Each site has:

* a location (`lat`, `lon`)
* `species_richness`
* `climate_refugia_score`
* `habitat_connectivity`
* `cost`
* `region`
* environmental features such as temperature, precipitation, and elevation

The default task is to choose 12 sites.

## Decision Tension

The best network is not simply the 12 richest sites. A useful monitoring network
also needs environmental coverage, reasonable cost, and low redundancy. Two
near-identical sites may both look strong on their own, but selecting both can
add less information than selecting complementary sites.

That tension is what makes the problem useful for optimization practice.
