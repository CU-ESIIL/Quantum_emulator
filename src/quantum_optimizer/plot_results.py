"""Output helpers for selected monitoring sites."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def write_selected_sites(
    selected_sites: pd.DataFrame,
    output_csv: str | Path,
    output_geojson: str | Path | None = None,
) -> None:
    """Write selected sites to CSV and, when lat/lon exist, GeoJSON."""

    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    selected_sites.to_csv(output_csv, index=False)

    if output_geojson is None or not {"lat", "lon"}.issubset(selected_sites.columns):
        return

    features = []
    for _, row in selected_sites.iterrows():
        properties = {
            key: _json_safe(value)
            for key, value in row.items()
            if key not in {"lat", "lon"}
        }
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(row["lon"]), float(row["lat"])],
                },
                "properties": properties,
            }
        )

    Path(output_geojson).write_text(
        json.dumps({"type": "FeatureCollection", "features": features}, indent=2)
    )


def _json_safe(value):
    if hasattr(value, "item"):
        return value.item()
    return value


def plot_site_selection(
    candidate_sites: pd.DataFrame,
    emulator_sites: pd.DataFrame,
    greedy_sites: pd.DataFrame,
    output_png: str | Path,
) -> bool:
    """Create a simple map-like scatter plot when matplotlib is available."""

    if not {"lat", "lon"}.issubset(candidate_sites.columns):
        return False

    output_png = Path(output_png)
    output_png.parent.mkdir(parents=True, exist_ok=True)

    try:
        import matplotlib.pyplot as plt
    except Exception:
        return _plot_site_selection_with_pillow(
            candidate_sites,
            emulator_sites,
            greedy_sites,
            output_png,
        )

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(
        candidate_sites["lon"],
        candidate_sites["lat"],
        s=26,
        c=candidate_sites.get("biological_value", candidate_sites.get("species_richness")),
        cmap="viridis",
        alpha=0.45,
        label="Candidate sites",
    )
    ax.scatter(
        greedy_sites["lon"],
        greedy_sites["lat"],
        s=72,
        facecolors="none",
        edgecolors="#f28e2b",
        linewidths=1.8,
        label="Greedy baseline",
    )
    ax.scatter(
        emulator_sites["lon"],
        emulator_sites["lat"],
        s=42,
        c="#4e79a7",
        marker="s",
        label="Quantum-inspired emulator",
    )
    ax.set_title("Ecological Monitoring Site Selection")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_png, dpi=180)
    plt.close(fig)
    return True


def _plot_site_selection_with_pillow(
    candidate_sites: pd.DataFrame,
    emulator_sites: pd.DataFrame,
    greedy_sites: pd.DataFrame,
    output_png: Path,
) -> bool:
    """Fallback plotter for environments without matplotlib."""

    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False

    width, height = 1000, 760
    margin = 70
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    lon_min, lon_max = candidate_sites["lon"].min(), candidate_sites["lon"].max()
    lat_min, lat_max = candidate_sites["lat"].min(), candidate_sites["lat"].max()

    def xy(row: pd.Series) -> tuple[float, float]:
        x = margin + (row["lon"] - lon_min) / (lon_max - lon_min) * (width - 2 * margin)
        y = height - margin - (row["lat"] - lat_min) / (lat_max - lat_min) * (height - 2 * margin)
        return float(x), float(y)

    draw.rectangle([margin, margin, width - margin, height - margin], outline="#aaaaaa", width=1)
    font = ImageFont.load_default()
    draw.text((margin, 25), "Ecological Monitoring Site Selection", fill="#222222", font=font)
    draw.text((margin, height - 42), "Longitude", fill="#444444", font=font)
    draw.text((18, margin), "Latitude", fill="#444444", font=font)

    for _, row in candidate_sites.iterrows():
        x, y = xy(row)
        draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill="#9ecae1", outline=None)

    for _, row in greedy_sites.iterrows():
        x, y = xy(row)
        draw.ellipse([x - 8, y - 8, x + 8, y + 8], outline="#f28e2b", width=3)

    for _, row in emulator_sites.iterrows():
        x, y = xy(row)
        draw.rectangle([x - 6, y - 6, x + 6, y + 6], fill="#4e79a7")

    legend_x, legend_y = width - 300, 35
    draw.ellipse([legend_x, legend_y, legend_x + 9, legend_y + 9], fill="#9ecae1")
    draw.text((legend_x + 18, legend_y - 2), "Candidate sites", fill="#333333", font=font)
    draw.ellipse([legend_x, legend_y + 24, legend_x + 14, legend_y + 38], outline="#f28e2b", width=2)
    draw.text((legend_x + 18, legend_y + 23), "Greedy baseline", fill="#333333", font=font)
    draw.rectangle([legend_x, legend_y + 53, legend_x + 12, legend_y + 65], fill="#4e79a7")
    draw.text((legend_x + 18, legend_y + 51), "Quantum-inspired emulator", fill="#333333", font=font)

    image.save(output_png)
    return True
