"""Build QUBO-style site-selection models from ecological decision tables."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

try:  # Optional: the demo works without dimod.
    import dimod
except Exception:  # pragma: no cover - exercised only when dimod is absent
    dimod = None


DEFAULT_VALUE_COLUMNS = [
    "species_richness",
    "climate_refugia_score",
    "habitat_connectivity",
]

DEFAULT_FEATURE_COLUMNS = [
    "mean_temp",
    "annual_precip",
    "elevation",
    "species_richness",
    "climate_refugia_score",
    "habitat_connectivity",
]


@dataclass
class SimpleBQM:
    """Small fallback representation for a binary quadratic model.

    A QUBO asks for binary decisions, usually 0/1. Here x_i = 1 means
    "select site i" and x_i = 0 means "do not select site i".
    """

    linear: dict[str, float]
    quadratic: dict[tuple[str, str], float]
    offset: float = 0.0
    vartype: str = "BINARY"

    @property
    def variables(self) -> list[str]:
        return list(self.linear)

    def energy(self, sample: dict[str, int]) -> float:
        total = self.offset
        total += sum(bias * sample.get(var, 0) for var, bias in self.linear.items())
        total += sum(
            bias * sample.get(u, 0) * sample.get(v, 0)
            for (u, v), bias in self.quadratic.items()
        )
        return float(total)


@dataclass
class QuboProblem:
    """Container tying a QUBO model back to its ecological site table."""

    bqm: object
    sites: pd.DataFrame
    target_count: int
    value_columns: list[str]
    feature_columns: list[str]
    variable_column: str = "variable"

    @property
    def variables(self) -> list[str]:
        return self.sites[self.variable_column].tolist()


def load_candidate_sites(path_or_table: str | Path | pd.DataFrame) -> pd.DataFrame:
    """Load a candidate site table from CSV or accept an existing DataFrame."""

    if isinstance(path_or_table, pd.DataFrame):
        table = path_or_table.copy()
    else:
        table = pd.read_csv(path_or_table)

    required = {"site_id", "cost"}
    missing = sorted(required - set(table.columns))
    if missing:
        raise ValueError(f"Candidate table is missing required columns: {missing}")

    return table


def _available_columns(table: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    return [col for col in columns if col in table.columns]


def _minmax(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.isna().all():
        return pd.Series(np.zeros(len(series)), index=series.index, dtype=float)
    numeric = numeric.fillna(numeric.median())
    low = float(numeric.min())
    high = float(numeric.max())
    if np.isclose(low, high):
        return pd.Series(np.zeros(len(series)), index=series.index, dtype=float)
    return (numeric - low) / (high - low)


def normalize_site_table(
    path_or_table: str | Path | pd.DataFrame,
    value_columns: Iterable[str] | None = None,
    feature_columns: Iterable[str] | None = None,
) -> tuple[pd.DataFrame, list[str], list[str]]:
    """Normalize decision columns to 0-1 scales.

    Biological value becomes a reward in the QUBO. Cost becomes a penalty.
    Environmental features are normalized before computing redundancy, so no
    single unit system dominates the similarity calculation.
    """

    table = load_candidate_sites(path_or_table)
    value_cols = _available_columns(table, value_columns or DEFAULT_VALUE_COLUMNS)
    if not value_cols:
        raise ValueError("At least one biological value column is required.")

    feature_cols = _available_columns(table, feature_columns or DEFAULT_FEATURE_COLUMNS)
    if not feature_cols:
        feature_cols = value_cols.copy()

    normalized = table.copy()
    for col in sorted(set(value_cols + feature_cols + ["cost"])):
        normalized[f"{col}_norm"] = _minmax(normalized[col])

    normalized["biological_value"] = normalized[[f"{c}_norm" for c in value_cols]].mean(axis=1)
    normalized["cost_norm"] = _minmax(normalized["cost"])
    normalized["variable"] = [f"x_{i}" for i in range(len(normalized))]
    return normalized, value_cols, feature_cols


def _add_linear(bqm: object, linear: dict[str, float], var: str, bias: float) -> None:
    if dimod is not None and isinstance(bqm, dimod.BinaryQuadraticModel):
        bqm.add_variable(var, bias)
    else:
        linear[var] = linear.get(var, 0.0) + bias


def _add_quadratic(
    bqm: object,
    quadratic: dict[tuple[str, str], float],
    var_a: str,
    var_b: str,
    bias: float,
) -> None:
    if var_a == var_b:
        _add_linear(bqm, {}, var_a, bias)
        return
    key = tuple(sorted((var_a, var_b)))
    if dimod is not None and isinstance(bqm, dimod.BinaryQuadraticModel):
        bqm.add_interaction(key[0], key[1], bias)
    else:
        quadratic[key] = quadratic.get(key, 0.0) + bias


def _feature_similarity(row_a: pd.Series, row_b: pd.Series, feature_columns: list[str]) -> float:
    values_a = row_a[[f"{c}_norm" for c in feature_columns]].to_numpy(dtype=float)
    values_b = row_b[[f"{c}_norm" for c in feature_columns]].to_numpy(dtype=float)
    distance = float(np.linalg.norm(values_a - values_b))
    max_distance = np.sqrt(len(feature_columns))
    if max_distance == 0:
        return 0.0
    return max(0.0, 1.0 - distance / max_distance)


def build_site_selection_qubo(
    path_or_table: str | Path | pd.DataFrame,
    target_count: int = 12,
    value_weight: float = 2.0,
    coverage_weight: float = 0.6,
    redundancy_weight: float = 1.2,
    cost_weight: float = 0.8,
    count_penalty: float = 2.5,
    value_columns: Iterable[str] | None = None,
    feature_columns: Iterable[str] | None = None,
) -> QuboProblem:
    """Create a QUBO/BQM for ecological monitoring site selection.

    The model minimizes energy. Good sites receive negative linear biases
    (rewards), while expensive or redundant combinations receive positive
    biases (penalties). This structure is quantum-ready because the same binary
    quadratic form can be sent to compatible quantum or hybrid solvers later,
    but running it here is a local emulation exercise.
    """

    sites, value_cols, feature_cols = normalize_site_table(
        path_or_table,
        value_columns=value_columns,
        feature_columns=feature_columns,
    )
    if not 1 <= target_count <= len(sites):
        raise ValueError("target_count must be between 1 and the number of candidate sites.")

    if dimod is not None:
        bqm = dimod.BinaryQuadraticModel({}, {}, 0.0, dimod.BINARY)
        linear: dict[str, float] = {}
        quadratic: dict[tuple[str, str], float] = {}
    else:
        linear = {}
        quadratic = {}
        bqm = SimpleBQM(linear=linear, quadratic=quadratic)

    for _, row in sites.iterrows():
        var = row["variable"]
        # A negative bias is a reward because QUBO solvers minimize energy.
        reward = value_weight * float(row["biological_value"])
        # Environmental coverage is approximated as preferring sites that score
        # strongly across the normalized environmental feature set.
        coverage = coverage_weight * float(
            row[[f"{c}_norm" for c in feature_cols]].mean()
        )
        cost = cost_weight * float(row["cost_norm"])
        _add_linear(bqm, linear, var, -reward - coverage + cost)

    # Penalize selecting too few or too many sites: strength * (sum(x) - k)^2.
    # For binary variables, x_i^2 = x_i, so this expands into linear and
    # quadratic terms.
    for var in sites["variable"]:
        _add_linear(bqm, linear, var, count_penalty * (1 - 2 * target_count))

    variables = sites["variable"].tolist()
    for i, var_a in enumerate(variables):
        for j in range(i + 1, len(variables)):
            var_b = variables[j]
            _add_quadratic(bqm, quadratic, var_a, var_b, 2 * count_penalty)

            similarity = _feature_similarity(sites.iloc[i], sites.iloc[j], feature_cols)
            # Redundancy is a pairwise penalty: two very similar selected sites
            # add less new information than two complementary sites.
            _add_quadratic(bqm, quadratic, var_a, var_b, redundancy_weight * similarity)

    if isinstance(bqm, SimpleBQM):
        bqm.offset = count_penalty * target_count**2
    elif dimod is not None:
        bqm.offset += count_penalty * target_count**2

    return QuboProblem(
        bqm=bqm,
        sites=sites,
        target_count=target_count,
        value_columns=value_cols,
        feature_columns=feature_cols,
    )
