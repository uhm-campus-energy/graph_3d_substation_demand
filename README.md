### Website:
https://uhm-campus-energy.github.io/graph_3d_substation_demand/

## Overview
An interactive 3D surface chart of substation electrical demand (kW). Each day is one row and each time of day is one column, so daily and seasonal load patterns are visible at a glance.

Before, you had to download all of the files to see the 3D graph. Now the GitHub Pages branch builds a website, so the chart opens directly in the browser.

## Using the chart
- **Date range:** pick a start and end date, then click **Update chart**.
- **Camera presets:** **Angled**, **Top-down**, **Front** and **Side** buttons switch the view. You can also drag to rotate and scroll to zoom.
- **Default view:** all data.

## Folder layout
| Folder / file | Purpose |
|---|---|
| `index.html` | The published page (the generated html) that's located in the Github-Page branch. |
| `input/` | Source CSV (`totalized_date_time_kw_matrix.csv`). |
| `output/` | Generated HTML from the script. |
| `scripts/generate_chart.py` | Builds the chart from the CSV. |
| `scripts/chart_template.html` | HTML/JS template the script fills with data. |
| `images/` | Screenshots used in documentation. |

## Input data format
A wide CSV with one row per day:
- A `Date` column (for example `2014/1/1 00:00:00`).
- One column per 15-minute interval, named `00:00`, `00:15`, ... `23:45`, holding kW values.

Small gaps are filled by interpolation along each day, then down each column for any fully missing day.

## Updating the chart
1. Install the requirement: `pip install pandas`
2. Replace or add the CSV in `input/`.
3. Run from the `scripts/` folder:
   ```
   python generate_chart.py
   ```
   Optional arguments: `--input`, `--output` and `--template` to override the default paths. If `input/` holds several CSVs, the first one alphabetically is used unless you pass `--input`.
4. The chart is written to `output/electrical_demand_3d_explorer.html`.
5. Publish it by copying that file to `index.html` (if it is the page you want live), then commit and push. GitHub Pages rebuilds the site automatically.
