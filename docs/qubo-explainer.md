# QUBO / Ising Explainer

A QUBO is a quadratic unconstrained binary optimization problem. The phrase is
long, but the idea is simple:

```text
choose 0 or 1 values that minimize an objective
```

QUBO models are widely used because many combinatorial problems can be expressed
as binary choices plus pairwise interactions. The tutorial by
[Glover, Kochenberger, and Du](https://arxiv.org/abs/1811.11538) is a useful
entry point, and [Lucas](https://arxiv.org/abs/1302.5843) shows how many
NP-hard problems can be written in related Ising forms.

For this demo, each binary variable represents a monitoring-site decision:

```text
x_17 = 1 means select site 17
x_17 = 0 means do not select site 17
```

## Rewards And Penalties

QUBO solvers minimize energy. To make a good ecological site attractive, the
model gives it a negative bias, which acts like a reward.

The demo uses:

* biological value as a reward
* environmental coverage as a reward
* cost as a penalty
* redundancy between similar selected sites as a pairwise penalty
* a target-count penalty to prefer selecting exactly 12 sites

In compact form, the model is trying to minimize an energy like:

```text
energy =
  - biological reward
  - environmental coverage reward
  + redundancy penalty
  + cost penalty
  + target-count penalty
```

The signs matter. Rewards lower energy because the solver minimizes. Penalties
raise energy when a candidate solution violates a preference.

## Why This Is Quantum-Ready

Quantum and quantum-inspired optimizers often accept binary quadratic models.
That means the same problem form can be used with a local emulator today and
with other compatible solvers later.

D-Wave's Ocean documentation describes this family as binary quadratic models
and notes that samplers accept such models and return variable assignments that
try to minimize the problem energy. See the
[D-Wave sampler documentation](https://docs.dwavequantum.com/en/latest/ocean/api_ref_system/samplers.html)
for the solver interface and the
[D-Wave concepts documentation](https://docs.dwavequantum.com/en/latest/concepts/index.html)
for the broader model vocabulary.

This is not proof that a quantum computer would outperform a classical method.
It is a way to practice the translation from environmental synthesis to a
solver-ready decision model.

## What The Emulator Does With The QUBO

After the QUBO is built, the local emulator searches for a low-energy set of
binary decisions. In this site-selection example, low energy means the selected
network balances the rewards and penalties encoded in the model:

* reward sites with high biological value
* reward environmental coverage
* penalize redundant site pairs
* penalize high cost
* penalize selecting too many or too few sites

Different weights change the meaning of "best." That is why the workflow is
useful for experimentation: researchers can rerun the same candidate table under
different ecological priorities and compare how the selected sites change.

## Why Baselines Are Required

A quantum-ready formulation is only useful if it is compared with something
understandable. This repo uses a greedy baseline because it is transparent: pick
the next site that looks best under a simple scoring rule. More serious studies
should also compare against established classical optimization tools, such as
mixed integer linear programming, simulated annealing, or domain tools like
Marxan and prioritizr.
