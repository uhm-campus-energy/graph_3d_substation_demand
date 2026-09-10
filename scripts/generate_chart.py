"""
generate_chart.py

Reads a totalized date/time kW matrix CSV from ../input/, builds an
interactive 3D Plotly surface (with date-range filtering and camera
presets), and writes a self-contained HTML file to ../output/.

Folder layout expected (relative to this script):
    graph_3d_substation_demand/
        input/    <- put the source .csv here
        output/   <- the generated .html lands here
        scripts/  <- this file, and chart_template.html, live here

Usage:
    python generate_chart.py
    python generate_chart.py --input ../input/my_file.csv --output ../output/demand_3d.html
"""

import argparse
import json
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_DIR = SCRIPT_DIR.parent / "input"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR.parent / "output"
TEMPLATE_PATH = SCRIPT_DIR / "chart_template.html"


def find_input_csv(input_dir: Path) -> Path:
    """Return the CSV to use: the first .csv file found in input_dir."""
    csvs = sorted(input_dir.glob("*.csv"))
    if not csvs:
        raise FileNotFoundError(
            f"No .csv file found in {input_dir}. Drop your date/time kW matrix "
            f"CSV in that folder, or pass --input path/to/file.csv"
        )
    if len(csvs) > 1:
        print(f"Note: multiple CSVs found in {input_dir}, using '{csvs[0].name}'. "
              f"Pass --input to choose a specific file.")
    return csvs[0]


def load_and_clean(csv_path: Path) -> pd.DataFrame:
    """Load the wide date x time-of-day matrix and fill small gaps."""
    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

    time_cols = [c for c in df.columns if c != "Date"]
    vals = df[time_cols].astype(float)

    # Fill gaps: first interpolate along each day (time-of-day), then
    # fall back to interpolating down each column for any fully-missing row.
    vals = vals.interpolate(axis=1, limit_direction="both")
    vals = vals.interpolate(axis=0, limit_direction="both")

    df[time_cols] = vals
    return df


def build_payload(df: pd.DataFrame) -> dict:
    time_cols = [c for c in df.columns if c != "Date"]
    return {
        "dates": df["Date"].tolist(),
        "times": time_cols,
        "z": df[time_cols].round(1).values.tolist(),
    }


def render_html(payload: dict, template_path: Path) -> str:
    template = template_path.read_text(encoding="utf-8")
    data_json = json.dumps(payload, separators=(",", ":"))
    if "__DATA_JSON__" not in template:
        raise ValueError(
            f"Template at {template_path} is missing the __DATA_JSON__ placeholder."
        )
    return template.replace("__DATA_JSON__", data_json)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=str, default=None,
                         help="Path to the source CSV (default: first .csv in ../input)")
    parser.add_argument("--output", type=str, default=None,
                         help="Path to write the HTML (default: ../output/electrical_demand_3d_explorer.html)")
    parser.add_argument("--template", type=str, default=str(TEMPLATE_PATH),
                         help="Path to the HTML template (default: chart_template.html next to this script)")
    args = parser.parse_args()

    input_path = Path(args.input) if args.input else find_input_csv(DEFAULT_INPUT_DIR)
    output_path = Path(args.output) if args.output else (
        DEFAULT_OUTPUT_DIR / "electrical_demand_3d_explorer.html"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Reading:  {input_path}")
    df = load_and_clean(input_path)
    print(f"Loaded {len(df):,} days x {len(df.columns) - 1} intervals/day")

    payload = build_payload(df)
    html = render_html(payload, Path(args.template))

    output_path.write_text(html, encoding="utf-8")
    size_mb = output_path.stat().st_size / 1e6
    print(f"Wrote:    {output_path}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
