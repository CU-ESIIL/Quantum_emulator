# Scientific Grounding

This site is a teaching project, but it should still sit on solid scientific
ground. The workflow combines three established ideas:

1. environmental data preparation,
2. spatial decision support,
3. binary optimization models used by quantum-inspired and hybrid solvers.

## Environmental Data Preparation

The emulator does not work directly on raw geospatial layers. It needs a
decision table. That is why harmonization remains part of the repository.

Analysis-ready geospatial systems such as the
[Open Data Cube](https://www.opendatacube.org/) emphasize consistent,
well-organized Earth observation data because downstream analyses depend on
stable spatial and temporal inputs. In this repo, the harmonizer plays a smaller
but similar role: it helps convert environmental layers into comparable site
features.

## Spatial Decision Support

The site-selection example is deliberately aligned with systematic conservation
planning. The classic framing from
[Margules and Pressey (2000)](https://www.nature.com/articles/35012251)
emphasizes that conservation decisions must account for representation,
persistence, threats, and broader landscape context.

Tools such as [Marxan](https://marxansolutions.org/) and
[prioritizr](https://prioritizr.net/) show how this becomes computational:
candidate planning units, biodiversity features, costs, constraints, penalties,
and solver outputs. The ecological monitoring demo is not a replacement for
those mature tools. It is a quantum-ready teaching analogue.

## QUBO And Ising Models

A QUBO represents a decision problem using binary variables and pairwise terms.
That form is attractive because many hard combinatorial problems can be mapped
into binary quadratic or Ising-style models.

Useful technical starting points:

* [Glover, Kochenberger, and Du](https://arxiv.org/abs/1811.11538) provide a
  tutorial on formulating and using QUBO models.
* [Lucas](https://arxiv.org/abs/1302.5843) surveys Ising formulations for many
  NP problems.
* [D-Wave Ocean documentation](https://docs.dwavequantum.com/en/latest/ocean/api_ref_system/samplers.html)
  describes samplers that accept quadratic models and return variable
  assignments.

## What "Quantum-Ready" Means

Quantum-ready means the problem has been expressed in a form that compatible
quantum-inspired, annealing, or hybrid solvers can accept. It does not mean a
quantum computer was used, and it does not imply quantum advantage.

The default workflow runs locally on classical hardware. That is intentional.
For near-term quantum technology, [Preskill's NISQ framing](https://arxiv.org/abs/1801.00862)
is a useful caution: current and near-term devices are scientifically important,
but broad practical advantage should not be assumed.

## What Counts As Evidence Here

The evidence in this teaching repo is not speedup. It is interpretability:

* Can we trace data from harmonized layers to decision-table columns?
* Can we explain what each binary variable means?
* Can we justify each reward and penalty?
* Can we compare emulator results with a classical baseline?
* Can we map selected sites back to geography?
* Can we rerun scenarios and see whether conclusions are stable?

That is the scholarly value of the emulator for EDS training. It gives
researchers a reproducible way to learn quantum-ready optimization while keeping
ecological interpretation and methodological caution at the center.
