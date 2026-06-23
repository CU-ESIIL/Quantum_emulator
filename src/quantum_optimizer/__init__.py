"""Quantum-ready optimization helpers for environmental site selection.

The package keeps the default path local and teachable: it can use D-Wave's
open-source modeling/sampling tools when installed, but it does not require a
D-Wave cloud account or claim quantum advantage.
"""

from .build_qubo import QuboProblem, build_site_selection_qubo, load_candidate_sites
from .classical_baseline import greedy_site_selection
from .score_solution import compare_solutions, score_selection
from .solve_emulator import solve_site_selection

__all__ = [
    "QuboProblem",
    "build_site_selection_qubo",
    "compare_solutions",
    "greedy_site_selection",
    "load_candidate_sites",
    "score_selection",
    "solve_site_selection",
]
