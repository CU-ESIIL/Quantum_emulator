#!/usr/bin/env python3
"""Run the local quantum-inspired emulator."""

import json
import sys
from pathlib import Path

_repo_root = next(p for p in Path(__file__).resolve().parents
                  if (p / "src" / "geospatial_harmonizer.py").exists())
sys.path.insert(0, str(_repo_root))

from src.quantum_optimizer import build_site_selection_qubo, solve_site_selection
from src.quantum_optimizer.plot_results import write_selected_sites


OUTPUT_DIR = Path(__file__).parent / "output"
CANDIDATE_CSV = OUTPUT_DIR / "candidate_sites.csv"
SELECTED_CSV = OUTPUT_DIR / "selected_sites_quantum_emulator.csv"
SELECTED_GEOJSON = OUTPUT_DIR / "selected_sites_quantum_emulator.geojson"
SOLUTION_JSON = OUTPUT_DIR / "quantum_emulator_solution.json"


def main() -> int:
    if not CANDIDATE_CSV.exists():
        raise FileNotFoundError(
            f"Missing {CANDIDATE_CSV}. Run 01_make_synthetic_site_table.py first."
        )

    problem = build_site_selection_qubo(CANDIDATE_CSV, target_count=12)
    result = solve_site_selection(problem, num_reads=40, sweeps=200, seed=11)

    write_selected_sites(result.selected_sites, SELECTED_CSV, SELECTED_GEOJSON)
    SOLUTION_JSON.write_text(
        json.dumps(
            {
                "solver": result.solver,
                "energy": result.energy,
                "selected_site_count": len(result.selected_sites),
                "selected_site_ids": result.selected_sites["site_id"].tolist(),
                "note": (
                    "This is a local quantum-inspired emulation run on classical "
                    "hardware, not proof of quantum advantage."
                ),
            },
            indent=2,
        )
    )
    print(f"Selected {len(result.selected_sites)} sites with {result.solver}")
    print(f"Wrote {SELECTED_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
