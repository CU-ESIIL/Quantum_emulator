#!/usr/bin/env python3
"""Compare the emulator selection with a transparent greedy baseline."""

import sys
from pathlib import Path

_repo_root = next(p for p in Path(__file__).resolve().parents
                  if (p / "src" / "geospatial_harmonizer.py").exists())
sys.path.insert(0, str(_repo_root))

import pandas as pd

from src.quantum_optimizer import compare_solutions, greedy_site_selection
from src.quantum_optimizer.plot_results import write_selected_sites


OUTPUT_DIR = Path(__file__).parent / "output"
CANDIDATE_CSV = OUTPUT_DIR / "candidate_sites.csv"
EMULATOR_CSV = OUTPUT_DIR / "selected_sites_quantum_emulator.csv"
GREEDY_CSV = OUTPUT_DIR / "selected_sites_greedy_baseline.csv"
GREEDY_GEOJSON = OUTPUT_DIR / "selected_sites_greedy_baseline.geojson"
COMPARISON_CSV = OUTPUT_DIR / "site_selection_comparison.csv"


def main() -> int:
    if not CANDIDATE_CSV.exists() or not EMULATOR_CSV.exists():
        raise FileNotFoundError(
            "Run 01_make_synthetic_site_table.py and 03_run_quantum_emulator.py first."
        )

    candidates = pd.read_csv(CANDIDATE_CSV)
    emulator_sites = pd.read_csv(EMULATOR_CSV)
    greedy_sites = greedy_site_selection(candidates, target_count=12)

    write_selected_sites(greedy_sites, GREEDY_CSV, GREEDY_GEOJSON)
    comparison = compare_solutions(
        candidates,
        {
            "quantum_inspired_emulator": emulator_sites,
            "greedy_classical_baseline": greedy_sites,
        },
    )
    comparison.to_csv(COMPARISON_CSV, index=False)
    print(f"Wrote baseline selection to {GREEDY_CSV}")
    print(f"Wrote comparison table to {COMPARISON_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
