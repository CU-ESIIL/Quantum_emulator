#!/usr/bin/env python3
"""Create a synthetic ecological monitoring candidate-site table."""

import sys
from pathlib import Path

_repo_root = next(p for p in Path(__file__).resolve().parents
                  if (p / "src" / "geospatial_harmonizer.py").exists())
sys.path.insert(0, str(_repo_root))

import numpy as np
import pandas as pd


OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_CSV = OUTPUT_DIR / "candidate_sites.csv"


def generate_synthetic_site_table(n_sites: int = 100, seed: int = 7) -> pd.DataFrame:
    """Generate a plausible site table for a Colorado-like study area."""

    rng = np.random.default_rng(seed)
    regions = np.array(["montane", "foothills", "plains", "riparian"])
    region = rng.choice(regions, size=n_sites, p=[0.34, 0.28, 0.24, 0.14])

    lat = rng.uniform(37.0, 41.0, size=n_sites)
    lon = rng.uniform(-109.0, -102.0, size=n_sites)
    elevation = np.clip(
        3350 - 420 * (lat - 37.0) + rng.normal(0, 420, size=n_sites),
        900,
        4200,
    )
    mean_temp = np.clip(17.5 - elevation / 430 + rng.normal(0, 1.4, size=n_sites), -4, 18)
    annual_precip = np.clip(260 + elevation * 0.18 + rng.normal(0, 80, size=n_sites), 180, 1050)

    region_bonus = pd.Series(region).map(
        {"montane": 18, "foothills": 10, "plains": 2, "riparian": 15}
    ).to_numpy()
    species_richness = np.clip(
        42 + region_bonus + annual_precip / 35 - np.abs(mean_temp - 8) * 1.6
        + rng.normal(0, 6, size=n_sites),
        8,
        95,
    )
    climate_refugia_score = np.clip(
        0.25 + (elevation - 900) / 5000 + annual_precip / 2500
        - np.maximum(mean_temp - 10, 0) / 30 + rng.normal(0, 0.08, size=n_sites),
        0,
        1,
    )
    habitat_connectivity = np.clip(
        0.38
        + (region == "riparian") * 0.24
        + (region == "montane") * 0.16
        - (region == "plains") * 0.08
        + rng.normal(0, 0.12, size=n_sites),
        0,
        1,
    )
    cost = np.clip(
        2800
        + elevation * 0.95
        + (region == "riparian") * 700
        + rng.normal(0, 520, size=n_sites),
        1200,
        9000,
    )

    return pd.DataFrame(
        {
            "site_id": [f"S{i:03d}" for i in range(1, n_sites + 1)],
            "lat": lat.round(6),
            "lon": lon.round(6),
            "species_richness": species_richness.round(2),
            "climate_refugia_score": climate_refugia_score.round(3),
            "habitat_connectivity": habitat_connectivity.round(3),
            "cost": cost.round(2),
            "region": region,
            "mean_temp": mean_temp.round(2),
            "annual_precip": annual_precip.round(2),
            "elevation": elevation.round(1),
        }
    )


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    table = generate_synthetic_site_table()
    table.to_csv(OUTPUT_CSV, index=False)
    print(f"Wrote {len(table)} candidate sites to {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
