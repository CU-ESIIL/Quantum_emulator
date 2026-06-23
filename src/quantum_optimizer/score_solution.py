"""Scoring utilities for selected ecological monitoring sites."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .build_qubo import normalize_site_table


def _mean_pairwise_distance(table: pd.DataFrame, feature_columns: list[str]) -> float:
    if len(table) < 2:
        return 0.0
    values = table[[f"{c}_norm" for c in feature_columns]].to_numpy(dtype=float)
    distances = []
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            distances.append(float(np.linalg.norm(values[i] - values[j])))
    return float(np.mean(distances))


def score_selection(
    selected_sites: pd.DataFrame,
    full_site_table: pd.DataFrame,
    label: str = "selection",
) -> dict[str, float | int | str]:
    """Summarize a solution in terms environmental scientists can inspect."""

    normalized_full, _, feature_cols = normalize_site_table(full_site_table)
    selected_ids = set(selected_sites["site_id"])
    selected = normalized_full[normalized_full["site_id"].isin(selected_ids)].copy()

    if selected.empty:
        raise ValueError("selected_sites does not overlap full_site_table by site_id.")

    regions = selected["region"].nunique() if "region" in selected.columns else 0
    return {
        "solution": label,
        "n_sites": int(len(selected)),
        "mean_biological_value": float(selected["biological_value"].mean()),
        "total_cost": float(selected["cost"].sum()),
        "mean_cost_norm": float(selected["cost_norm"].mean()),
        "mean_environmental_distance": _mean_pairwise_distance(selected, feature_cols),
        "regions_represented": int(regions),
    }


def compare_solutions(
    full_site_table: pd.DataFrame,
    selections: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Build a comparison table for emulator and classical baseline outputs."""

    rows = [
        score_selection(selected, full_site_table, label=label)
        for label, selected in selections.items()
    ]
    return pd.DataFrame(rows)
