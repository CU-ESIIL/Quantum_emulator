"""Local quantum-inspired solvers for site-selection QUBOs."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .build_qubo import QuboProblem, SimpleBQM


@dataclass
class SolverResult:
    """Selected sites and solver metadata."""

    selected_sites: pd.DataFrame
    sample: dict[str, int]
    energy: float
    solver: str


def _energy(bqm: object, sample: dict[str, int]) -> float:
    if hasattr(bqm, "energy"):
        return float(bqm.energy(sample))
    if isinstance(bqm, SimpleBQM):
        return bqm.energy(sample)
    raise TypeError("Unsupported BQM object.")


def _sample_with_target(variables: list[str], target_count: int, rng: np.random.Generator) -> dict[str, int]:
    chosen = set(rng.choice(variables, size=target_count, replace=False))
    return {var: int(var in chosen) for var in variables}


def _repair_to_target(
    problem: QuboProblem,
    sample: dict[str, int],
    target_count: int,
) -> dict[str, int]:
    """Adjust a sample to exactly the requested number of selected sites."""

    repaired = sample.copy()
    sites = problem.sites.set_index("variable")
    selected = [var for var, value in repaired.items() if value]
    if len(selected) > target_count:
        ranked = sorted(
            selected,
            key=lambda var: (
                float(sites.loc[var, "biological_value"]) - float(sites.loc[var, "cost_norm"])
            ),
        )
        for var in ranked[: len(selected) - target_count]:
            repaired[var] = 0
    elif len(selected) < target_count:
        unselected = [var for var, value in repaired.items() if not value]
        ranked = sorted(
            unselected,
            key=lambda var: (
                float(sites.loc[var, "biological_value"]) - float(sites.loc[var, "cost_norm"])
            ),
            reverse=True,
        )
        for var in ranked[: target_count - len(selected)]:
            repaired[var] = 1
    return repaired


def _local_search(
    problem: QuboProblem,
    num_reads: int,
    sweeps: int,
    seed: int | None,
) -> tuple[dict[str, int], float]:
    rng = np.random.default_rng(seed)
    variables = problem.variables
    target = problem.target_count
    best_sample: dict[str, int] | None = None
    best_energy = float("inf")

    for _ in range(num_reads):
        sample = _sample_with_target(variables, target, rng)
        current_energy = _energy(problem.bqm, sample)

        for _ in range(sweeps):
            selected = [var for var, value in sample.items() if value]
            unselected = [var for var, value in sample.items() if not value]
            if not selected or not unselected:
                break

            drop = rng.choice(selected)
            add = rng.choice(unselected)
            candidate = sample.copy()
            candidate[drop] = 0
            candidate[add] = 1
            candidate_energy = _energy(problem.bqm, candidate)

            if candidate_energy <= current_energy or rng.random() < 0.02:
                sample = candidate
                current_energy = candidate_energy

        if current_energy < best_energy:
            best_sample = sample
            best_energy = current_energy

    assert best_sample is not None
    return best_sample, best_energy


def _solve_with_neal(
    problem: QuboProblem,
    num_reads: int,
    seed: int | None,
) -> tuple[dict[str, int], float] | None:
    try:
        import neal
    except Exception:
        return None

    sampler = neal.SimulatedAnnealingSampler()
    kwargs = {"num_reads": num_reads}
    if seed is not None:
        kwargs["seed"] = seed
    sampleset = sampler.sample(problem.bqm, **kwargs)
    sample = dict(sampleset.first.sample)
    sample = _repair_to_target(problem, sample, problem.target_count)
    return sample, _energy(problem.bqm, sample)


def solve_site_selection(
    problem: QuboProblem,
    num_reads: int = 100,
    sweeps: int = 400,
    seed: int | None = 42,
    prefer_neal: bool = True,
) -> SolverResult:
    """Solve the QUBO locally.

    If dwave-neal is installed, this uses local simulated annealing. Otherwise
    it falls back to randomized swap search. Both paths run on classical
    hardware and are meant for training, not as evidence of quantum speedup.
    """

    neal_result = _solve_with_neal(problem, num_reads, seed) if prefer_neal else None
    if neal_result is not None:
        sample, energy = neal_result
        solver = "dwave-neal simulated annealing"
    else:
        sample, energy = _local_search(problem, num_reads=num_reads, sweeps=sweeps, seed=seed)
        solver = "local randomized swap search"

    selected_variables = {var for var, value in sample.items() if value}
    selected = problem.sites[problem.sites["variable"].isin(selected_variables)].copy()
    selected = selected.sort_values("site_id").reset_index(drop=True)
    return SolverResult(selected_sites=selected, sample=sample, energy=energy, solver=solver)
