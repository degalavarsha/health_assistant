"""Download NHANES SAS transport (.xpt) files from CDC.

Cycles:
  P  = 2017-March 2020 pre-pandemic, files named P_<COMPONENT>.xpt  (Public/2017)
  L  = August 2021-August 2023,      files named <COMPONENT>_L.xpt  (Public/2021)

NCHS advises against pooling the 2021-2023 cycle with older ones, so they are
stored in separate folders and meant to be used as separate train/test sets.

Usage:  python ingest/download_nhanes.py [--out data/nhanes]
Missing files (404) are reported, not fatal: file names differ between cycles.
"""
import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{year}/DataFiles/{name}.xpt"

# component -> description
COMPONENTS = {
    "DEMO": "demographics (age, sex, weights)",
    "BMX": "body measures",
    "BPXO": "blood pressure (oscillometric)",
    "BPX": "blood pressure (older auscultatory name, may not exist)",
    "CBC": "complete blood count",
    "GHB": "HbA1c",
    "GLU": "fasting glucose",
    "HDL": "HDL cholesterol",
    "TCHOL": "total cholesterol",
    "TRIGLY": "triglycerides and LDL",
    "BIOPRO": "standard biochemistry profile",
    "FERTIN": "ferritin",
    "TFR": "soluble transferrin receptor",
    "VID": "vitamin D",
    "INS": "insulin",
    "HSCRP": "high-sensitivity CRP",
    "FOLATE": "serum/RBC folate",
    "DIQ": "diabetes questionnaire (diagnosed or not)",
    "DR1TOT": "diet recall day 1 totals",
    "DR2TOT": "diet recall day 2 totals",
}

CYCLES = {
    "P": {"year": 2017, "name": lambda c: f"P_{c}"},   # 2017-Mar 2020 (already contains 2017-18 "J")
    "L": {"year": 2021, "name": lambda c: f"{c}_L"},   # 2021-2023
    "I": {"year": 2015, "name": lambda c: f"{c}_I"},   # 2015-2016
    "H": {"year": 2013, "name": lambda c: f"{c}_H"},   # 2013-2014
    "G": {"year": 2011, "name": lambda c: f"{c}_G"},   # 2011-2012
    "F": {"year": 2009, "name": lambda c: f"{c}_F"},   # 2009-2010
}
# Older cycles use auscultatory BPX; lab methods (CBC, HbA1c, ferritin) can differ
# between cycles, so keep the cycle as a feature/group when pooling.


def fetch(url: str, dest: Path) -> str:
    if dest.exists() and dest.stat().st_size > 0:
        return "exists"
    req = urllib.request.Request(url, headers={"User-Agent": "ai-health-assistant-research"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except Exception as e:  # network errors
        return f"error: {e}"
    if not data.startswith(b"HEADER RECORD"):
        return "not an XPT file"
    dest.write_bytes(data)
    return f"ok {len(data) / 1e6:.1f} MB"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[2] / "data" / "nhanes"))
    ap.add_argument("--cycles", nargs="+", default=list(CYCLES), choices=list(CYCLES))
    args = ap.parse_args()

    missing = []
    for cyc in args.cycles:
        cfg = CYCLES[cyc]
        folder = Path(args.out) / cyc
        folder.mkdir(parents=True, exist_ok=True)
        for comp, desc in COMPONENTS.items():
            name = cfg["name"](comp)
            status = fetch(BASE.format(year=cfg["year"], name=name), folder / f"{name}.xpt")
            print(f"[{cyc}] {name:<14} {status:<14} {desc}")
            if not (status.startswith("ok") or status == "exists"):
                missing.append(f"{cyc}:{name} ({status})")
    print("\nNot available:", ", ".join(missing) if missing else "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
