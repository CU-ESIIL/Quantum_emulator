"""Simple classical baselines for comparing quantum-inspired selections."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .build_qubo import normalize_site_table


def _redundancy(candidate: pd.Series, selected: pd.DataFrame, feature_columns: list[str]) -> float:
    if selected.empty:
        return 0.0
    candidate_values = candidate[[f"{c}_norm" for c in feature_columns]].to_numpy(dtype=float)
    selected_values = selected[[f"{c}_norm" for c in feature_columns]].to_numpy(dtype=float)
    distances = np.linalg.norm(selected_values - candidate_values, axis=1)
    similarities = 1.0 - distances / np.sqrt(len(feature_columns))
    return float(np.clip(similarities, 0, 1).mean())


def greedy_site_selection(
    path_or_table: str | pd.DataFrame,
    target_count: int = 12,
    value_weight: float = 2.0,
    coverage_weight: float = 0.6,
    redundancy_weight: float = 1.2,
    cost_weight: float = 0.8,
) -> pd.DataFrame:
    """Choose sites one at a time using a transparent scoring rule."""

    sites, _, feature_cols = normalize_site_table(path_or_table)
    remaining = sites.copy()
    selected_indices: list[int] = []

    for _ in range(target_count):
        if remaining.empty:
            break

        selected = sites.loc[selected_indices] if selected_indices else sites.iloc[0:0]
        scored_rows = []
        for _, row in remaining.iterrows():
            coverage = float(row[[f"{c}_norm" for c in feature_cols]].mean())
            score = (
                value_weight * float(row["biological_value"])
                + coverage_weight * coverage
                - redundancy_weight * _redundancy(row, selected, feature_cols)
                - cost_weight * float(row["cost_norm"])
            )
            scored_rows.append((score, row.name))

        _, best_index = max(scored_rows, key=lambda item: item[0])
        selected_indices.append(best_index)
        remaining = remaining.drop(index=best_index)

    return sites.loc[selected_indices].sort_values("site_id").reset_index(drop=True)
