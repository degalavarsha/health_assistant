# Free lab/vitals datasets, APIs and risk equations for health risk screening (as of 2026-10-31)

## 1. NHANES cycles, file names, download patterns, weights, Python packages

### Takeaway
NHANES is the best free lab+vitals source. The cycle list now runs 1999-2000 through 08/2021-08/2023 (suffix `_L`), plus a 2025-2027 cycle that is listed but has no data yet. Prepandemic 2017-March 2020 is a separate combined release (prefix `P_`). Plain pip-installable NHANES packages exist, but none is named exactly "nhanes", and most are small, community-maintained projects.

### Cited Findings
- Cycles listed on the CDC page: 2025-2027, 08/2021-08/2023, 2017-March 2020 (Pre-Pandemic), 2019-2020, 2017-2018, 2015-2016, 2013-2014, 2011-2012, 2009-2010, 2007-2008, 2005-2006, 2003-2004, 2001-2002 and 1999-2000. Nothing newer than 2025-2027 is listed. — [CDC NHANES home](https://wwwn.cdc.gov/nchs/nhanes/default.aspx)
- 2025-2027 is in early stages. Only brochures and consent documents are posted. Demographics, dietary, exam, lab and questionnaire data are all "not yet available", and no release dates are given. — [NHANES 2025-2027 page](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2025-2027)
- Page URL patterns: `https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component={Demographics|Dietary|Examination|Laboratory|Questionnaire}&Cycle=YYYY-YYYY`. For 2021-2023 the page-fetch tool also accepted `&CycleBeginYear=2021`. — [CDC NHANES home](https://wwwn.cdc.gov/nchs/nhanes/default.aspx)
- 08/2021-08/2023 lab files, all `_L` suffix. XPT URL pattern `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/<FILE>.xpt`, with documentation at the same path as `<FILE>.htm`. The files are: CBC_L (5-part CBC), GHB_L (HbA1c), GLU_L (fasting plasma glucose), HDL_L, TCHOL_L, TRIGLY_L (LDL and triglycerides), FERTIN_L, TFR_L, FOLATE_L (RBC folate), FOLFMS_L (serum folate forms), FFMR_L, VID_L (vitamin D), INS_L, HSCRP_L, BIOPRO_L (standard biochemistry), ALB_CR_L, FASTQX_L (fasting questionnaire), PBCD_L and others. 32 lab files in total. No vitamin B12 file or serum-iron file appears in this list. — [Lab files 2021-2023](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&CycleBeginYear=2021)
- Dietary 2021-2023: DR1TOT_L (11.4 MB), DR2TOT_L (5.8 MB), DR1IFF_L (64.2 MB), DR2IFF_L (56.4 MB), DRXFCD_L, DSQTOT_L, DSQIDS_L, all at `/Nchs/Data/Nhanes/Public/2021/DataFiles/<FILE>.xpt`. — [Dietary files 2021-2023](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Dietary&Cycle=2021-2023)
- Prepandemic 2017-March 2020: `P_` prefix, with URL pattern `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_<FILE>.xpt` (the host was inferred from the page's links). Present files are P_CBC, P_GHB, P_GLU, P_HDL, P_TCHOL, P_TRIGLY, P_FERTIN, P_TFR, P_BIOPRO, P_INS and P_HSCRP. P_VID (vitamin D) and a B12 file were not found on the page. — [Lab files 2017-2020](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&Cycle=2017-2020)
- 2017-2018 (suffix `_J`): VID_J, FERTIN_J, TFR_J, FOLATE_J, FOLFMS_J and FETIB_J (serum iron/TIBC) exist. No B12 file was found. — [Lab files 2017-2018](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&Cycle=2017-2018)
- Suffix convention: 1999-2000 none or `_A`, with letters increasing by cycle (2017-2018 is `_J`, prepandemic is `P_`, 2021-2023 is `_L`). Letters for DEMO, BMX, BPX and BPQ follow the same pattern. The suffix itself was only verified for `_J`, `P_` and `_L` in the fetched pages.
- Weights:
  - Use the weight of the smallest subpopulation that contains all your variables. WTINT2YR covers interview-only variables, WTMEC2YR covers exam variables, and WTSAF2YR covers the fasting subsample (needed for fasting glucose, triglycerides and LDL).
  - Dietary weights are WTDRD1 (day 1) and WTDR2D (both days).
  - 08/2021-08/2023 adds a phlebotomy weight, WTPH2YR, for phlebotomy-based lab data.
  - Prepandemic uses the weight WTMECPRP. Combine 2015-2016 with prepandemic as a 5.2-year weight: 2/5.2 for 2015-2016 and 3.2/5.2 for prepandemic.
  - From 2001-2002 onward, divide 2-year weights by the number of cycles combined.
  - NCHS generally advises against combining 08/2021-08/2023 with other cycles, because of the 1.5-year gap and pandemic disruption. The page does not cover PSU/strata (SDMVPSU, SDMVSTRA) and refers to the Variance Estimation module.
  — [NHANES weighting tutorial](https://wwwn.cdc.gov/nchs/nhanes/tutorials/weighting.aspx)
- Python packages that exist on PyPI or GitHub:
  - `pynhanes` has a 1.0.0 CLI (`pynhanes-downloader -o XPT -a 2003,2005,...`). Older 0.0.x releases were notebook-based. Accelerometry data is opt-in (about 18 GB). — [PyPI pynhanes](https://pypi.org/project/pynhanes)
  - `cdc-nhanes-dl` installs from GitHub, not PyPI (`pip install git+https://github.com/ink-waffle/cdc-nhanes-dl`). It snapshots public NHANES to Parquet, about 6 GB and 15-40 minutes. — [PyPI cdc-nhanes-dl](https://pypi.org/project/cdc-nhanes-dl/)
  - `pandas-nhanes` (0.1.8) gives a cleaned subset with caching and `get_variables`/`get_dataset`. — [PyPI pandas-nhanes](https://pypi.org/project/pandas-nhanes/)
  - `nhanes-dl` (0.0.18) downloads codebooks to pandas and links mortality data. — [PyPI nhanes-dl](https://pypi.org/project/nhanes-dl)
  - `NHANES-Downloader` (mrwyattii) is a legacy GitHub script. — [GitHub](https://github.com/mrwyattii/NHANES-Downloader)
  - A package literally named "nhanes" was not found on PyPI by the search. Nothing named "nhanes-pytorch" turned up either.
  - NHANES XPT files can be read directly with `pandas.read_sas(url, format="xport")`. This is standard pandas behaviour and was not re-verified here.

### Inferences
- A robust pipeline can hit CDC XPT URLs directly. Build file names from a per-cycle map (`{"2017-2020": ("P_", ""), "2021-2023": ("", "_L")}`), because there is no third-party dependency risk that way.
- A nutrient-status label needs different files per cycle. Ferritin, TFR and folate exist in `_J`, `P_` and `_L`. Vitamin D exists in `_J` and `_L` but not in P_. B12 was not located in any cycle checked. Plan on ferritin, TFR, iron and vitamin D as labels, and treat B12 as a separate task.
- Cross-cycle pooling: the `P_` and `_L` releases have different weight variables (WTMECPRP vs WTMEC2YR/WTPH2YR). Avoid naively stacking them. Instead, train on pooled data and report weighted metrics per cycle.

### Gaps
- Exact B12 file names (`VITB12_*`/`B12_*`) and which cycles carry them were not verified. The cycles I checked (2017-2018, prepandemic, 2021-2023) did not list one.
- DEMO, BMX, BPX file availability per cycle was not fetched. The names DEMO_L, BMX_L, BPXO_L (oscillometric BP, replacing BPX in recent cycles), P_DEMO, P_BMX and P_BPXO are from memory and unverified. Check these before coding.
- Release dates for 2025-2027 data are not published.
- Whether NHANES lab methods changed between cycles for HbA1c, ferritin and vitamin D (affecting comparability) was not researched.

## 2. Other free or access-controlled datasets

### Takeaway
Free with no access barrier: UCI Heart Disease, CDC Diabetes Health Indicators and BRFSS. Free with a credentialing step: MIMIC-IV, eICU, Framingham (BioLINCC) and All of Us. Paid: UK Biobank, with a platform closure noted. Only NHANES combines a lab panel, vitals and public download.

### Cited Findings
- UCI Heart Disease (Cleveland etc.): CC BY 4.0, 303 instances, 13 features, 125.9 KB zip. Download via `/static/public/45/heart+disease.zip` or `ucimlrepo.fetch_ucirepo(id=45)`. — [UCI](https://archive.ics.uci.edu/dataset/45/heart+disease)
- CDC Diabetes Health Indicators (UCI ID 891): 253,680 instances, BRFSS-derived survey data (self-reported, no lab values), classes Diabetes/Pre-diabetes/Healthy. The metadata is inconsistent: 21 features listed, "35 features" in the text. The license is not stated ("see linked dataset"). The source link points to the BRFSS 2014 page, though I believe the data is 2015 (unverified). Get it with `fetch_ucirepo(id=891)` or from [Kaggle](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset). — [UCI](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators)
- BRFSS 2024: 457,670 records, ASCII and SAS Transport files dated August 2025, plus codebook and weighting guidance. Self-reported, no labs. — [CDC BRFSS 2024](https://cdc.gov/brfss/annual_data/annual_2024.html)
- MIMIC-IV v3.1 (published 2024-10-11): PhysioNet Credentialed Health Data License 1.5.0. Requires credentialed PhysioNet account, CITI "Data or Specimens Only Research" training and a signed DUA. 364,627 patients, 546,028 hospitalizations, 94,458 ICU stays at BIDMC, 2008-2022. Also on BigQuery. — [PhysioNet MIMIC-IV](https://physionet.org/content/mimiciv/)
- eICU-CRD v2.0 (2019): same license and credentialing. More than 200,000 ICU admissions, 208 US hospitals, 2014-2015. — [PhysioNet eICU](https://physionet.org/content/eicu-crd/)
- Framingham Heart Study cohort on BioLINCC: free registration, but the requester must get full or expedited IRB/ethics approval (no waivers or exemptions), and commercial-use restrictions are flagged. 5,209 original participants, exams 1-32, events through 2018, last updated 2025-07-21. — [BioLINCC](https://biolincc.nhlbi.nih.gov/studies/framcohort/)
- All of Us: tiers are Public (aggregate), Registered (individual-level EHR, wearables, surveys, physical measurements) and Controlled (adds genomics and unshifted dates). Access is by "data passport" through the Researcher Workbench. Cost, participant count and lab availability were not on the page. — [All of Us data access](https://www.researchallofus.org/data-tools/data-access/)
- UK Biobank: an access fee of GBP 500 for the first 3 years (GBP 175/year after), exclusive of VAT, and data are accessible only via the UKB-RAP. Compute is billed separately, with GBP 40 of starting credit. Reduced fees exist for students and for researchers from lower-income countries. UKB-RAP was reported as "currently closed", with re-opening phased "from September 2026". Verify the current status. — [UK Biobank fees](https://www.ukbiobank.ac.uk/use-our-data/fees/) (details via search summary, snapshot undated)

### Inferences
- For an MVP, UCI Heart Disease, Pima and the CDC Diabetes Indicators are fine for quick baselines. They lack the lab depth, so NHANES should be the main training set.
- MIMIC-IV and eICU are ICU cohorts and a poor population match for outpatient screening. They are useful only for lab-pattern work.

### Gaps
- Pima Indians Diabetes: I did not verify its license, source page or size. From memory it has 768 rows and 8 features, and Kaggle hosts a copy (the original is a UCI/NIDDK dataset). Check before use.
- Kaggle heart datasets other than UCI: sizes and licenses not checked.
- All of Us cohort size and lab/vitals coverage: not verified from the official page.
- The sources for the UCI Diabetes dataset's year and licence (CC0 on Kaggle?) are unverified.

## 3. Validated risk equations and open implementations

### Takeaway
Open-source implementations exist for QRISK3 (R), PREVENT (Python and R) and Pooled Cohort Equations (R). A ready Python PCE package was not verified. SCORE2, FINDRISC, ADA and ATP III/IDF code was not located and would need to be written from the published papers or guidelines.

### Cited Findings
- `pyprevent` (kingrc15): pure-Python (numpy and pandas) AHA PREVENT implementation, Python 3.9+. It returns 10- and 30-year risk for total CVD, ASCVD and heart failure. Cholesterol must be in mmol/L, and the smoking coding is the opposite of older calculators. — [GitHub kingrc15/pyprevent](https://github.com/kingrc15/pyprevent)
- R: `preventr` (martingmayer, on CRAN) implements PREVENT and permits comparison with PCE. `PooledCohort` (bcjaeger, on CRAN) implements the 2013 PCE, the 2018 revision and PREVENT. — [preventr manual](https://martingmayer.r-universe.dev/preventr/doc/manual.html); [PooledCohort manual](https://search.r-project.org/CRAN/packages/PooledCohort/PooledCohort.pdf)
- QRISK3: unofficial R package (CRAN) by Li, Sperrin and van Staa, validated against the original C/SAS algorithm. GitHub: YanLiUK/QRISK3 and YanLiUK/QRISK3_valid (GPL-3). ClinRisk says users must confirm any implementation matches qrisk.org. — [F1000Research article](https://f1000research.com/articles/8-2139)
- WHO anaemia thresholds (pre-2024): Hb below 110 g/L for children 6-59 months and pregnant women, below 115 for children 5-11, below 120 for children 12-14 and non-pregnant women, below 130 for men. The March 2024 guideline changed the cutoff for children 6-23 months to below 105 g/L and kept second-trimester pregnancy as a separate entry (value not confirmed). — [WHO guideline via PAHO](https://www.paho.org/en/documents/guideline-haemoglobin-cutoffs-define-anaemia-individuals-and-populations); [BMJ summary via search](https://bestpractice-bmj-com.bibliotheek.ehb.be/topics/en-gb/94/criteria)

### Inferences
- A PCE implementation is short (published coefficients per sex/race group). It is easier to port from `PooledCohort` than to find a Python library.
- The 2024 WHO change affects only young children, so adult anaemia screening can use the long-standing cutoffs. Smoking altitude adjustments are out of scope.

### Gaps
- No official guideline URLs were fetched for ADA diabetes criteria (HbA1c 6.5, FPG 126, prediabetes 5.7-6.4), ATP III/IDF/harmonized metabolic syndrome, the ADA risk test, FINDRISC or SCORE2. Values come from general knowledge and are not cited here.
- No GitHub implementation of SCORE2, FINDRISC, ATP III or the ADA risk test was found.
- Official ACC/AHA PCE and SCORE2 publication links were not retrieved.
- WHO ferritin thresholds were not found.

## 4. LOINC and reference ranges

### Takeaway
LOINC is free to use and redistribute with attribution, but downloading needs a free account and acceptance of the terms. No free authoritative reference-range database was identified.

### Cited Findings
- LOINC is available at no cost under the license at loinc.org/license. Downloads require a free account and agreement to the terms of service. Some third-party content (for example assessment scales) can carry separate copyright. The LOINC and RELMA names are Regenstrief trademarks. A redistribution notice is required. — secondary summaries via [LOINC license search](https://loinc.org/license) (direct fetch returned HTTP 403, so this wording is unverified against the primary page); [Getting LOINC](https://loinc.org/get-started/getting-loinc/)
- NHANES documentation pages (.htm per file) give LOINC codes and lab method notes for each variable. This is general knowledge, not checked in this session.

### Inferences
- Map NHANES variables to LOINC for interoperability. Keep a small in-repo mapping table with the required attribution notice rather than bundling the full LOINC table.

### Gaps
- Primary-source LOINC license text could not be fetched.
- No reference-range source (for example the NHANES-derived CALIPER, or Mayo or labs' published ranges) was researched.
- Current LOINC release version and date not verified.
