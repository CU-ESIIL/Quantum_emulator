#!/usr/bin/env python3
"""Map candidate and selected monitoring sites."""

import sys
from pathlib import Path

_repo_root = next(p for p in Path(__file__).resolve().parents
                  if (p / "src" / "geospatial_harmonizer.py").exists())
sys.path.insert(0, str(_repo_root))

import pandas as pd

from src.quantum_optimizer.plot_results import plot_site_selection


OUTPUT_DIR = Path(__file__).parent / "output"
CANDIDATE_CSV = OUTPUT_DIR / "candidate_sites.csv"
EMULATOR_CSV = OUTPUT_DIR / "selected_sites_quantum_emulator.csv"
GREEDY_CSV = OUTPUT_DIR / "selected_sites_greedy_baseline.csv"
OUTPUT_PNG = OUTPUT_DIR / "harmonized_visualization.png"


def main() -> int:
    required = [CANDIDATE_CSV, EMULATOR_CSV, GREEDY_CSV]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Run previous workflow steps first. Missing: {missing}")

    candidates = pd.read_csv(CANDIDATE_CSV)
    emulator_sites = pd.read_csv(EMULATOR_CSV)
    greedy_sites = pd.read_csv(GREEDY_CSV)
    made_plot = plot_site_selection(candidates, emulator_sites, greedy_sites, OUTPUT_PNG)
    if made_plot:
        print(f"Wrote map to {OUTPUT_PNG}")
    else:
        print("Map skipped because matplotlib or lat/lon columns were unavailable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
