# Agents And Emulator Workflows

This repository keeps the agentic AI connection, but the center of the website
is now the quantum-emulator workflow.

The practical division of labor is:

```text
AI agent support -> data preparation and workflow scaffolding
quantum-inspired emulator -> decision-space exploration
human researchers -> interpretation and scientific judgment
```

## Why Agents Still Matter

Environmental decision problems are rarely ready for optimization when a
working group first defines them. The data may live in different formats, use
different coordinate systems, require documentation, or need to be transformed
into a candidate-site table.

An AI agent can help with that surrounding workflow:

* finding and checking data sources
* writing harmonization scripts
* generating decision-table preparation code
* documenting assumptions
* running lightweight validation
* keeping workflow outputs in predictable folders

The agent does not replace scientific review. It accelerates the construction of
an inspectable workflow.

## Why The Repository Is The System

The repository is the durable scientific object. It contains the code,
documentation, instructions, outputs, and tests that make the workflow
reproducible.

For this project, the repository defines:

* how ecological monitoring sites are represented
* how binary decision variables are constructed
* how a QUBO rewards biological value and coverage
* how cost and redundancy become penalties
* how emulator output is compared with a classical baseline
* how selected sites are mapped back to geography

That structure matters more than any single chat response. The model helps build
the system; the system is what can be inspected, shared, and rerun.

## Guardrails For This Project

The agent instructions in `AGENTS.md` are part of the methods record. They tell
future agents to:

* keep the emulator workflow central
* preserve the harmonizer as a data-preparation layer
* avoid claims of quantum advantage or speedup
* keep D-Wave cloud access out of the default path
* compare emulator results with a clear classical baseline
* document new workflows and append to the prompt action log

These constraints keep the project practical and honest.

## From Data To Decision

The scientific value of this repository is not that an AI model or emulator
produces an answer by itself. The value is that a working group can trace the
path from environmental synthesis to a candidate-site table, from that table to
a binary optimization model, and from solver output back to ecological
interpretation.

That is the point of the agentic structure here: not less rigor, but a clearer
and faster way to build workflows that researchers can inspect.
