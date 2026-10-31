# NYC Film Permits: Lights, Camera, Street Closures
Mini-Project 2 working prototype · Information Visualization, NYU Tandon

Interactive D3 dashboard with three linked views of the NYC Open Data **Film Permits** dataset
(dataset ID `tg4x-b46p`):

| View | Question (from proposal) | Encoding |
|---|---|---|
| Subcategory scatter | RQ1 footprint | x = permits (log), y = median shoot duration, area = avg. streets held, hue = category |
| Borough bars | RQ2 geography | length = permits, segment lightness = duration bin |
| Monthly timeline | RQ3 time | x = month, y = permits, hue = category; drag to brush a date range |

**Linking:** click a borough bar, a scatter dot or a category in the legend, or drag on the timeline. Every other view
updates. Chips in the header show active filters; Reset clears everything.

## Run it

1. **Get the data.** Download the CSV from NYC Open Data (search "Film Permits", ID `tg4x-b46p`), e.g.
   `https://data.cityofnewyork.us/api/v3/views/tg4x-b46p/export.csv?accessType=DOWNLOAD`
   (or use Export > CSV on the dataset page).
2. **Clean it.** `pip install pandas`, then in this folder:
   `python3 prep_data.py path/to/downloaded.csv`
   Read what it prints: it shows the column mapping, rows kept/dropped and why, and writes
   `data/permits_clean.csv` + `data/meta.json`. If it says it cannot find a column, edit `ALIASES` at the top of
   `prep_data.py`.
3. **Open it.** `python3 -m http.server 8000`, then visit http://localhost:8000
   (a browser blocks loading data from a `file://` page; if you do open the file directly, use the file picker it shows).

## Host it (GitHub Pages)
1. Create a public GitHub repo and upload everything in this folder, **including** `data/permits_clean.csv`
   (about 10 MB, well under GitHub's limit).
2. Repo Settings > Pages > Deploy from branch `main` / root.
3. After a minute the site is at `https://<username>.github.io/<repo>/`. Open it in a private window to confirm it loads.

## Cleaning rules (shown in the dashboard footer)
Only `Shooting Permit` events (use `--all-types` to keep all); rows missing start, end, borough or category dropped;
durations <= 0 or > 336 h dropped; empty subcategory = "Unspecified"; streets = number of "between" segments in the
free-text ParkingHeld column (approximate). Category = top 4 by permit count + "Other".

## How the code works (so you can explain it)
- `prep_data.py`: matches column names ignoring case/spaces, parses dates, computes duration and street count, writes a small CSV.
- `index.html` > `indexData()`: turns rows into typed arrays (category, borough, subcategory, month, duration bin).
- `state`: one object holding the active filters. Every interaction edits it and calls `render()`.
- `compute()`: a single pass over all rows that builds the data for all three views. Each view **ignores the filter on
  its own dimension** (standard cross-filtering), so you can still see and switch to the other options.
- Medians come from a 0.1 h histogram per subcategory instead of sorting, which keeps the brush smooth.
- `renderScatter / renderBars / renderTimeline`: D3 joins with 220 ms transitions (off while dragging the brush).
- Radius is proportional to sqrt(value) so dot **area** is proportional to streets held.

## Known gaps (planned for the final)
Scatter has click-select but no lasso; tooltips are basic; narrow screens shrink the timeline text; accessibility
tuning and the two usability tests happen after the peer session.

## Credits
D3.js v7 (Mike Bostock, ISC license) · NYC Open Data, Mayor's Office of Media and Entertainment ·
AI assistance: Claude Sonnet 5.5 (Anthropic) wrote the first version of this code; edit this line to describe what you changed.
