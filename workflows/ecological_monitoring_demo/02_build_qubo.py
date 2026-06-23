#!/usr/bin/env python3
"""Build the QUBO for the ecological monitoring site-selection problem."""

import json
import sys
from pathlib import Path

_repo_root = next(p for p in Path(__file__).resolve().parents
                  if (p / "src" / "geospatial_harmonizer.py").exists())
sys.path.insert(0, str(_repo_root))

from src.quantum_optimizer import build_site_selection_qubo


OUTPUT_DIR = Path(__file__).parent / "output"
CANDIDATE_CSV = OUTPUT_DIR / "candidate_sites.csv"
SUMMARY_JSON = OUTPUT_DIR / "qubo_summary.json"
NORMALIZED_CSV = OUTPUT_DIR / "candidate_sites_normalized.csv"


def main() -> int:
    if not CANDIDATE_CSV.exists():
        raise FileNotFoundError(
            f"Missing {CANDIDATE_CSV}. Run 01_make_synthetic_site_table.py first."
        )

    problem = build_site_selection_qubo(CANDIDATE_CSV, target_count=12)
    problem.sites.to_csv(NORMALIZED_CSV, index=False)

    bqm = problem.bqm
    summary = {
        "target_count": problem.target_count,
        "n_candidate_sites": len(problem.sites),
        "n_variables": len(problem.variables),
        "n_linear_terms": len(getattr(bqm, "linear", {})),
        "n_quadratic_terms": len(getattr(bqm, "quadratic", {})),
        "value_columns": problem.value_columns,
        "feature_columns": problem.feature_columns,
        "note": (
            "A binary variable x_i = 1 means select site i. The QUBO rewards "
            "biological value and environmental coverage, and penalizes cost, "
            "redundancy, and missing the requested number of sites."
        ),
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2))
    print(f"Wrote QUBO summary to {SUMMARY_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
