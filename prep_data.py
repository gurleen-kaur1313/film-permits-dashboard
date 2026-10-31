#!/usr/bin/env python3
"""
prep_data.py - clean the raw NYC Film Permits CSV into the compact file the dashboard loads.

Usage:
    python3 prep_data.py path/to/raw_film_permits.csv
    python3 prep_data.py path/to/raw_film_permits.csv --all-types     # keep every event type

Output (written to ./data/):
    permits_clean.csv   one row per permit: id,start,borough,category,sub,dur_h,streets
    meta.json           cleaning report (row counts, what was dropped and why)

Cleaning rules (these are reported in meta.json and shown in the dashboard footer):
    1. Keep only EventType == "Shooting Permit" (unless --all-types).
    2. Drop rows missing start time, end time, borough or category.
    3. Drop rows whose duration (End - Start) is <= 0 or > 336 h (14 days).
    4. Empty SubCategory becomes "Unspecified".
    5. streets = number of street segments in ParkingHeld (count of "between", else
       comma-separated parts, else 0). ParkingHeld is free text, so this is approximate.

Requires: pandas (pip install pandas)
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

MAX_HOURS = 336  # 14 days; longer permits are treated as data-entry outliers

# Header matching ignores case, spaces and punctuation, so "Start Date Time",
# "StartDateTime" and "startdatetime" are all the same column.
ALIASES = {
    "id": ["eventid"],
    "type": ["eventtype"],
    "start": ["startdatetime", "startdate", "start"],
    "end": ["enddatetime", "enddate", "end"],
    "borough": ["borough"],
    "category": ["category"],
    "sub": ["subcategoryname", "subcategory"],
    "parking": ["parkingheld", "parkinghelp"],
}
REQUIRED = ["start", "end", "borough", "category"]


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def find_columns(columns):
    lookup = {norm(c): c for c in columns}
    found = {}
    for key, names in ALIASES.items():
        for n in names:
            if n in lookup:
                found[key] = lookup[n]
                break
    return found


def count_streets(text):
    """Approximate number of street segments in the free-text ParkingHeld field."""
    if not isinstance(text, str) or not text.strip():
        return 0
    n = len(re.findall(r"\bbetween\b", text, flags=re.I))
    if n:
        return n
    return len([p for p in text.split(",") if p.strip()])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_csv")
    ap.add_argument("--all-types", action="store_true", help="keep all event types")
    ap.add_argument("--out", default=str(Path(__file__).parent / "data"))
    args = ap.parse_args()

    raw = pd.read_csv(args.raw_csv, dtype=str, keep_default_na=False, low_memory=False)
    cols = find_columns(raw.columns)
    print("Columns found in your file:", list(raw.columns))
    print("Mapped to:", cols)

    missing = [k for k in REQUIRED if k not in cols]
    if missing:
        sys.exit(f"ERROR: could not find column(s) for {missing}. Edit ALIASES in prep_data.py "
                 f"to match the headers printed above.")
    if "sub" not in cols:
        print("WARNING: no SubCategory column found; every permit will be 'Unspecified' "
              "and the scatter will have a single dot.")
    if "parking" not in cols:
        print("WARNING: no ParkingHeld column found; streets will be 0 and dot area will not encode anything.")

    report = {"source": Path(args.raw_csv).name, "raw_rows": int(len(raw)), "dropped": {}}
    df = pd.DataFrame(index=raw.index)
    for k, c in cols.items():
        df[k] = raw[c].str.strip()

    # 1. event type
    if "type" in df and not args.all_types:
        keep = df["type"].str.casefold() == "shooting permit"
        if keep.sum() == 0:
            sys.exit("ERROR: no 'Shooting Permit' rows. Event types present: "
                     f"{sorted(df['type'].unique())[:15]}. Re-run with --all-types or adjust the filter.")
        report["dropped"]["not a shooting permit"] = int((~keep).sum())
        df = df[keep]
        report["event_types_kept"] = ["Shooting Permit"]
    else:
        report["event_types_kept"] = sorted(df["type"].unique().tolist()) if "type" in df else ["(no type column)"]

    # 2. parse dates, require key fields
    df["start_dt"] = pd.to_datetime(df["start"], errors="coerce", format="mixed")
    df["end_dt"] = pd.to_datetime(df["end"], errors="coerce", format="mixed")
    bad = (df["start_dt"].isna() | df["end_dt"].isna() | (df["borough"] == "") | (df["category"] == ""))
    report["dropped"]["missing start/end/borough/category"] = int(bad.sum())
    df = df[~bad].copy()

    # 3. duration
    df["dur_h"] = (df["end_dt"] - df["start_dt"]).dt.total_seconds() / 3600
    bad = (df["dur_h"] <= 0) | (df["dur_h"] > MAX_HOURS)
    report["dropped"][f"duration <= 0 or > {MAX_HOURS} h"] = int(bad.sum())
    df = df[~bad].copy()

    # 4-5. tidy fields and derived street count
    df["sub"] = df["sub"].replace("", "Unspecified") if "sub" in df else "Unspecified"
    df["streets"] = df["parking"].map(count_streets).clip(upper=255) if "parking" in df else 0
    df["borough"] = df["borough"].str.title()
    df["category"] = df["category"].str.title()
    if "id" not in df:
        df["id"] = range(len(df))

    out = pd.DataFrame({
        "id": df["id"],
        "start": df["start_dt"].dt.strftime("%Y-%m-%dT%H:%M"),
        "borough": df["borough"],
        "category": df["category"],
        "sub": df["sub"],
        "dur_h": df["dur_h"].round(2),
        "streets": df["streets"].astype(int),
    })

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    out.to_csv(outdir / "permits_clean.csv", index=False)

    report.update({
        "kept_rows": int(len(out)),
        "date_min": out["start"].min(),
        "date_max": out["start"].max(),
        "boroughs": out["borough"].value_counts().to_dict(),
        "top_categories": out["category"].value_counts().head(8).to_dict(),
        "n_subcategories": int(out["sub"].nunique()),
        "share_with_streets": round(float((out["streets"] > 0).mean()), 3),
        "generated": datetime.now().isoformat(timespec="seconds"),
    })
    (outdir / "meta.json").write_text(json.dumps(report, indent=2))

    print(f"\nKept {report['kept_rows']:,} of {report['raw_rows']:,} rows")
    for k, v in report["dropped"].items():
        print(f"  dropped {v:,}: {k}")
    print("Top categories:", report["top_categories"])
    print("Boroughs:", report["boroughs"])
    print(f"Permits with a street count > 0: {report['share_with_streets']:.0%}")
    print(f"Wrote {outdir/'permits_clean.csv'} and {outdir/'meta.json'}")


if __name__ == "__main__":
    main()
