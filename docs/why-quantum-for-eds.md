# Why Quantum for EDS?

Environmental data science often turns messy, high-dimensional information into
decisions: where to monitor, where to restore habitat, how to allocate sampling
effort, or how to compare management scenarios.

Many of those decisions can be written as optimization problems. A monitoring
network, for example, is a set of yes/no choices:

```text
select site S001? yes or no
select site S002? yes or no
select site S003? yes or no
```

That binary structure is why quantum-inspired methods are worth learning. They
provide a way to practice translating environmental synthesis outputs into
decision models that can be explored with local emulators today and quantum or
hybrid systems later.

## The EDS Connection

In an ESIIL-style workflow, a working group might first build a geospatial data
cube or harmonized table from climate, biodiversity, land cover, access, and
cost layers. The next question is not only "what patterns exist?" but "what
decision should we make with those patterns?"

This repo focuses on that handoff from data to decision.

## What To Keep In Mind

Quantum-ready does not mean quantum advantage. It means the problem has been
structured in a way that can be represented with binary variables and quadratic
relationships. That structure is useful for learning, comparison, and future
experimentation, even when every computation in this repo runs on classical
hardware.
