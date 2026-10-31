"""Build one adult training table from the downloaded NHANES cycles.

Cycles: F 2009-10, G 2011-12, H 2013-14, I 2015-16, P 2017-Mar 2020, L 2021-23.
(The old 2017-18 "J" files are already inside P and are NOT used here.)

Column names are harmonised across cycles; blood pressure is the mean of the
2nd..nth reading (first reading dropped, per usual practice) when available.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "nhanes"

CYCLES = {  # code -> (folder, filename builder, start year)
    "F": (lambda c: f"{c}_F", 2009), "G": (lambda c: f"{c}_G", 2011),
    "H": (lambda c: f"{c}_H", 2013), "I": (lambda c: f"{c}_I", 2015),
    "P": (lambda c: f"P_{c}", 2017), "L": (lambda c: f"{c}_L", 2021),
}


def _read(cycle: str, comp: str) -> pd.DataFrame:
    name = CYCLES[cycle][0](comp)
    return pd.read_sas(DATA / cycle / f"{name}.xpt", format="xport")


def _mean_bp(df: pd.DataFrame, sys_cols: list[str], dia_cols: list[str]) -> pd.DataFrame:
    s = df[sys_cols].replace(0, np.nan)
    d = df[dia_cols].replace(0, np.nan)
    # drop the first reading when at least one more exists
    sbp = s.iloc[:, 1:].mean(axis=1).fillna(s.iloc[:, 0])
    dbp = d.iloc[:, 1:].mean(axis=1).fillna(d.iloc[:, 0])
    return pd.DataFrame({"SEQN": df["SEQN"], "sbp": sbp, "dbp": dbp})


def load_cycle(cycle: str) -> pd.DataFrame:
    demo = _read(cycle, "DEMO")
    wcol = "WTMECPRP" if cycle == "P" else "WTMEC2YR"
    out = pd.DataFrame({
        "SEQN": demo["SEQN"], "age": demo["RIDAGEYR"], "sex": demo["RIAGENDR"],
        "race": demo["RIDRETH1"], "mec_weight": demo[wcol],
    })
    bmx = _read(cycle, "BMX")[["SEQN", "BMXBMI", "BMXWAIST"]]
    bmx.columns = ["SEQN", "bmi", "waist_cm"]
    out = out.merge(bmx, on="SEQN", how="left")

    bp = _read(cycle, "BPXO" if cycle in ("P", "L") else "BPX")
    if cycle in ("P", "L"):
        bp = _mean_bp(bp, ["BPXOSY1", "BPXOSY2", "BPXOSY3"], ["BPXODI1", "BPXODI2", "BPXODI3"])
    else:
        bp = _mean_bp(bp, ["BPXSY1", "BPXSY2", "BPXSY3", "BPXSY4"],
                      ["BPXDI1", "BPXDI2", "BPXDI3", "BPXDI4"])
    out = out.merge(bp, on="SEQN", how="left")

    for comp, cols in {
        "TCHOL": {"LBXTC": "total_chol"}, "HDL": {"LBDHDD": "hdl"},
        "GHB": {"LBXGH": "hba1c"}, "GLU": {"LBXGLU": "fasting_glucose"},
        "CBC": {"LBXHGB": "hemoglobin"}, "DIQ": {"DIQ010": "diabetes_dx"},
    }.items():
        d = _read(cycle, comp)
        out = out.merge(d[["SEQN", *cols]].rename(columns=cols), on="SEQN", how="left")

    tg = _read(cycle, "TRIGLY")
    tgcol = "LBXTLG" if "LBXTLG" in tg.columns else "LBXTR"
    tg = tg[["SEQN", tgcol]].rename(columns={tgcol: "triglycerides"})
    out = out.merge(tg, on="SEQN", how="left")
    out["cycle"] = cycle
    out["cycle_year"] = CYCLES[cycle][1]
    return out


def build_dataset(cycles: list[str] | None = None, adults_only: bool = True) -> pd.DataFrame:
    frames = [load_cycle(c) for c in (cycles or list(CYCLES))]
    df = pd.concat(frames, ignore_index=True)
    if adults_only:
        df = df[df["age"] >= 20]
    return df.reset_index(drop=True)
