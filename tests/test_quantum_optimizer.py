"""Lightweight tests for the ecological monitoring optimizer workflow."""

import importlib.util
from pathlib import Path

import pandas as pd

from src.quantum_optimizer import (
    build_site_selection_qubo,
    compare_solutions,
    greedy_site_selection,
    score_selection,
    solve_site_selection,
)


REPO_ROOT = Path(__file__).parent.parent
SYNTHETIC_SCRIPT = (
    REPO_ROOT
    / "workflows"
    / "ecological_monitoring_demo"
    / "01_make_synthetic_site_table.py"
)


def _load_synthetic_module():
    spec = importlib.util.spec_from_file_location("synthetic_sites", SYNTHETIC_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_synthetic_site_table_generation():
    module = _load_synthetic_module()
    table = module.generate_synthetic_site_table(n_sites=25, seed=3)
    assert len(table) == 25
    assert {
        "site_id",
        "lat",
        "lon",
        "species_richness",
        "climate_refugia_score",
        "habitat_connectivity",
        "cost",
        "region",
        "mean_temp",
        "annual_precip",
        "elevation",
    }.issubset(table.columns)
    assert table["site_id"].is_unique


def test_qubo_construction_returns_model():
    module = _load_synthetic_module()
    table = module.generate_synthetic_site_table(n_sites=20, seed=4)
    problem = build_site_selection_qubo(table, target_count=5)
    assert problem.target_count == 5
    assert len(problem.variables) == 20
    assert hasattr(problem.bqm, "linear")
    assert hasattr(problem.bqm, "quadratic")


def test_emulator_returns_requested_number_of_sites():
    module = _load_synthetic_module()
    table = module.generate_synthetic_site_table(n_sites=30, seed=5)
    problem = build_site_selection_qubo(table, target_count=6)
    result = solve_site_selection(problem, num_reads=12, sweeps=50, seed=6, prefer_neal=False)
    assert len(result.selected_sites) == 6
    assert set(result.selected_sites["site_id"]).issubset(set(table["site_id"]))


def test_scoring_works():
    module = _load_synthetic_module()
    table = module.generate_synthetic_site_table(n_sites=25, seed=7)
    selected = table.head(5)
    score = score_selection(selected, table, label="test")
    assert score["solution"] == "test"
    assert score["n_sites"] == 5
    assert score["mean_biological_value"] >= 0


def test_greedy_baseline_and_comparison_work():
    module = _load_synthetic_module()
    table = module.generate_synthetic_site_table(n_sites=25, seed=8)
    greedy = greedy_site_selection(table, target_count=5)
    other = table.tail(5).copy()
    comparison = compare_solutions(
        table,
        {"greedy": greedy, "other": other},
    )
    assert len(greedy) == 5
    assert isinstance(comparison, pd.DataFrame)
    assert set(comparison["solution"]) == {"greedy", "other"}
