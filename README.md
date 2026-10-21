Website: https://uhm-campus-energy.github.io/graph_3d_substation_demand/
 ### Website:
https://uhm-campus-energy.github.io/graph_3d_substation_demand/

## Overview
An interactive 3D surface chart of substation electrical demand (kW). Each day is one row and each time of day is one column, so daily and seasonal load patterns are visible at a glance.

Before, you had to download all of the files to see the 3D graph. Now the GitHub Pages branch builds a website, so the chart opens directly in the browser.

## GitHub Pages branch
The site is built from the **`Github-Pages`** branch with Jekyll (theme: minima). The `main` branch does not publish a site.

- `index.html` is the published chart page. It is a self-contained file with the data embedded, so the site needs no server.
- `_config.yml`, `_layouts/`, `_includes/`, `about.markdown` and `404.html` are the Jekyll site files (navigation, footer, other pages).
- The site rebuilds automatically on every push to `Github-Pages`. Check progress under the repository's **Actions** tab. If a build fails, that tab shows the log.
- Pages must be set to deploy from this branch under **Settings > Pages**.

## Using the chart
- **Date range:** pick a start and end date, then click **Update chart**.
- **Camera presets:** **Angled**, **Top-down**, **Front** and **Side** buttons switch the view. You can also drag to rotate and scroll to zoom.
- **Default view:** all data.

## Folder layout
| Folder / file | Purpose |
|---|---|
| `index.html` | The published page (the generated HTML) on the `Github-Pages` branch. |
| `_config.yml`, `_layouts/`, `_includes/`, `about.markdown`, `404.html` | Jekyll site files. |
| `input/` | Source CSV (`totalized_date_time_kw_matrix.csv`). |
| `output/` | Generated HTML from the script (not tracked on the `Github-Pages` branch). |
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
5. Publish it: copy that file over `index.html`, then commit and push to the `Github-Pages` branch. GitHub Pages rebuilds the site automatically.
