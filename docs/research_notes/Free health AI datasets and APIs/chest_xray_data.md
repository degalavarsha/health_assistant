# Chest X-ray datasets, pretrained models, best practices and licensing for a multi-label CXR classifier

Research date: 2026-10-31. About 17 tool calls; many license texts were NOT directly verified (see Gaps). Items without a source are in Gaps, not Cited Findings.

## Dataset inventory (size, labels, license, access, commercial use)

### Takeaway
Every large, high-quality CXR dataset (CheXpert, CheXpert Plus, MIMIC-CXR-JPG, VinDr-CXR, BRAX, PadChest) is gated behind a research-use agreement or credentialing. Stanford and PadChest bar commercial use outright. For the PhysioNet sets (MIMIC-CXR-JPG, VinDr-CXR, BRAX) the credentialed license does not clearly permit a public app, and I could not verify its commercial terms. For a public app, treat all of them as research and validation only unless the owner grants written permission.

### Cited Findings
- **NIH ChestX-ray14 (owned):** 112,120 frontal images from 30,805 patients, one center (NIH Clinical Center); 14 labels mined from reports by NLP, not hand-annotated — [arXiv 1907.12720](https://arxiv.org/pdf/1907.12720); [Papers with Code](https://paperswithcode.com/dataset/chestx-ray14). NIH distributes train_val_list.txt and test_list.txt (86,524 train/val and 25,596 test per the HF mirror) — [HF mirror](https://huggingface.co/datasets/alkzar90/NIH-Chest-X-ray-dataset); [hyper.ai](https://hyper.ai/en/datasets/16729). Sources conflict on license: the HF card says no restrictions but asks for credit and a citation to the CVPR 2017 paper; another copy says "unknown"; an aggregator says MIT — [HF card](https://huggingface.co/datasets/alkzar90/NIH-Chest-X-ray-dataset); [HF blame view](https://huggingface.co/datasets/alkzar90/NIH-Chest-X-ray-dataset/blame/main/README.md); [AIOZ](https://aioz.network/blog/nih-chest-x-ray-frontal-images-for-multi-disease-detection). CC0 was NOT confirmed.
- **CheXpert (Stanford):** 224,316 radiographs from 65,240 patients, Stanford Health Care, Oct 2002 to Jul 2017, with reports. Download is via a login link on the AIMI page, and a "Commercial Use of AIMI Datasets" page exists — [Stanford AIMI](https://aimi.stanford.edu/datasets/chexpert-chest-x-rays). AIMI's shared datasets are free for non-commercial research, with a separate process for commercial use — [search summary of AIMI](https://aimi.stanford.edu/shared-datasets).
- **CheXpert Plus:** 223,228 unique image-report pairs from 187,711 studies and 64,725 patients per the arXiv paper (AIMI lists 223,462). The Stanford Dataset Research Use Agreement bars commercial use, allows research only, and forbids redistribution — [arXiv 2405.19538](https://arxiv.org/pdf/2405.19538); [AIMI CheXpert Plus](https://aimi.stanford.edu/datasets/chexpert-plus).
- **MIMIC-CXR-JPG v2.1.0 (Mar 2024):** 377,110 JPGs linked to about 227,827 reports. Labels come from the CheXpert and NegBio rule-based labelers: 13 findings plus "No Finding", coded 1.0 / 0.0 / -1.0 (uncertain) / blank. Includes a recommended train/val/test split and a radiologist-labeled test set. Access: credentialed PhysioNet user, CITI "Data or Specimens Only Research" training, and a signed DUA. License is PhysioNet Credentialed Health Data License 1.5.0; DUA terms include no sharing and no re-identification — [PhysioNet](https://physionet.org/content/mimic-cxr-jpg/2.1.0/). The page does not address commercial use.
- **VinDr-CXR:** 18,000 released images (15,000 train, 3,000 test), adults only, from 100,000+ raw scans. 28 labels: 22 local findings with bounding boxes and 6 global labels, including TB, pneumonia, COPD and "No finding". Train set has 3 independent radiologists per image. Test set is a consensus of 5. Same credentialed PhysioNet license and DUA — [PhysioNet](https://physionet.org/content/vindr-cxr/1.0.0/).
- **PadChest (BIMCV, Spain):** about 160,000 images from about 67,000 patients (San Juan Hospital, 2009-2017). Free for research on request. It cannot be sold, non-academic use is approved case by case, and redistribution needs written permission — [BIMCV agreement](https://bimcv.cipf.es/?p=4923); [arXiv 1901.07441](https://arxiv.org/abs/1901.07441v2).
- **BRAX (Brazil, Albert Einstein hospital):** 40,967 images, 24,959 studies, 19,351 patients, 14 findings derived by NLP from Portuguese reports and verified by radiologists. PhysioNet "Database Credentialed Access", v1.1.0 (June 2022). License text not retrieved — [PMC9364309](https://pmc.ncbi.nlm.nih.gov/articles/PMC9364309); [PhysioNet](https://physionet.org/content/brax/).
- **RSNA Pneumonia (2018):** images come from NIH ChestX-ray14, relabeled by radiologists (STR and MD.ai). RSNA's page says use is allowed for academic research and education and for "other commercial or non-commercial purposes" if attribution requirements are met — [RSNA](https://www.rsna.org/artificial-intelligence/ai-image-challenge/RSNA-Pneumonia-Detection-Challenge-2018). The NIH-source terms still apply to the underlying images (inference).
- **TBX11K:** the project page says CC BY 4.0. Only train and validation sets are released, and the download is reportedly 512x512 — [mmcheng.net](https://mmcheng.net/tb/); [mednet docs](https://mednet.readthedocs.io/en/stable/_modules/mednet/data/classify/tbx11k.html).
- **ChestX-Det10:** 3,543 images with instance-level annotations for 10 categories, reportedly a subset of ChestX-ray14. Deepwise's own license was NOT retrieved. A third-party HF mirror tags apache-2.0 — [arXiv 2006.10550](https://arxiv.org/abs/2006.10550v1); [HF mirror](https://huggingface.co/datasets/MedOtter/ChestX-Det/discussions).

### Inferences
- Suggested roles: train on NIH (owned), plus CheXpert / MIMIC-CXR if research-only is acceptable. For external validation use VinDr-CXR (radiologist-labeled, a different country and different labelers), PadChest or BRAX (different continents), and the MIMIC radiologist-labeled test set. RSNA, ChestX-Det and ChestX-ray14 share NIH-derived images, so they are NOT independent external sets for a model trained on NIH.
- If the app is public or commercial, safe options narrow to datasets you can verify as permissive (possibly TBX11K for TB only, RSNA with attribution), or you obtain written commercial permission from the data owners.
- Label noise differs by source: NLP-derived (NIH, CheXpert, MIMIC, BRAX, PadChest) versus radiologist-annotated (VinDr-CXR, ChestX-Det, RSNA). Prefer radiologist labels for validation.

### Gaps
- NIH license text (Box page) not verified; CC0 claim is unconfirmed.
- CheXpert label set (14 observations with uncertainty), the CheXpert validation set (200 studies) and the CheXpert registration form: I did not retrieve these from a source. They are from memory, so verify.
- The Stanford Research Use Agreement text, and the PhysioNet 1.5.0 license text (commercial and app clauses), were not read.
- SIIM-ACR pneumothorax (Kaggle) license and rules: not found. COVID datasets (BIMCV-COVID19, COVID-19 Image Data Collection, COVIDx): not researched.
- Kaggle rule terms for RSNA were not retrieved. BRAX license not retrieved. ChestX-Det license not retrieved.
- Whether NIH's official split is patient-level was not confirmed from a source (the metadata CSV has patient IDs; verify yourself).

## Pretrained open models and weights

### Takeaway
TorchXRayVision is the most practical drop-in (DenseNet121 "all" weights, 18 outputs). Its weights were trained on datasets with research-only terms, and its license was not shown on the page I fetched. BiomedCLIP is MIT but deployed use is explicitly out of scope. RAD-DINO moved to a Microsoft research license, and Google's CXR Foundation needs acceptance of HAI-DEF terms.

### Cited Findings
- **TorchXRayVision:** classifiers `densenet121-res224-{all,rsna,nih,pc,chex,mimic_nb,mimic_ch}` and `resnet50-res512-all`. Load with `xrv.models.DenseNet(weights="densenet121-res224-all")`. Input preprocessing: `xrv.datasets.normalize(img, 255)`, single channel, `XRayCenterCrop()`, `XRayResizer(224)`. 18 pathologies: Atelectasis, Consolidation, Infiltration, Pneumothorax, Edema, Emphysema, Fibrosis, Effusion, Pneumonia, Pleural_Thickening, Cardiomegaly, Nodule, Mass, Hernia, Lung Lesion, Fracture, Lung Opacity, Enlarged Cardiomediastinum. For non-"all" weights, untrained outputs "predict randomly", so use only the dataset's `.pathologies`. The page frames it as for researchers and the license is not shown on that page — [GitHub mlmed/torchxrayvision](https://github.com/mlmed/torchxrayvision). It also ships a PSPNet anatomy segmenter (ChestX-Det) and baseline JF Healthcare and Stanford CheXpert DenseNets (same page).
- **BiomedCLIP:** MIT license; pretrained on PMC-15M figure-caption pairs (general biomedical, not CXR-specific); load via open_clip `hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224`. The card states "Any deployed use case of the model — commercial or otherwise — is currently out of scope" — [HF model card](https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224).
- **RAD-DINO (microsoft/rad-dino):** license tag is now "msrla" (Microsoft Research License) after a change on 2024-08-19; earlier README said MIT; some mirrors still show MIT — [HF discussion](https://huggingface.co/microsoft/rad-dino/discussions/1); [HF repo](https://huggingface.co/microsoft/rad-dino/tree/main).
- **Google CXR Foundation:** weights at `google/cxr-foundation` on Hugging Face, gated by acceptance of the Health AI Developer Foundations terms (approval immediate) plus a Prohibited Use Policy; Google calls them open-weight and allows packaging into your own service; terms copy dated 2024-11-15 — [model card](https://developers.google.com/health-ai-developer-foundations/cxr-foundation/model-card); [terms](https://developers.google.com/health-ai-developer-foundations/terms); [FAQ](https://developers.google.com/health-ai-developer-foundations/faqs).
- **MONAI Model Zoo:** the repo is Apache-licensed and bundles carry their own license and data license files, so check each — [GitHub model-zoo](https://github.com/project-monai/model-zoo); [bundle docs](https://monai.readthedocs.io/en/stable/bundle_intro.html). No CXR multi-label classifier bundle was found in my search.

### Inferences
- Fine-tuning from TorchXRayVision weights or a RAD-DINO/CXR Foundation backbone is likely a faster route than training from scratch, but check the weights' license chain: weights trained on CheXpert/MIMIC/PadChest may inherit research-only terms (inference, unverified).
- Comparing your NIH-trained model against the TorchXRayVision `densenet121-res224-all` baseline on VinDr-CXR is a cheap external-validation sanity check.

### Gaps
- TorchXRayVision library and weights license (the repo has a LICENSE file I did not read). Benchmarks in its BENCHMARKS.md were not read.
- CheXNet-like repos (e.g., arnoweng/CheXNet, Keras/PyTorch reimplementations): not researched; licenses unknown.
- Other CXR foundation models (e.g., CheXagent, MedImageInsight, BiomedParse) not researched.

## Best practices and known pitfalls

### Takeaway
NIH labels are noisy NLP output, so test-set metrics can look good while being clinically weak. Models can exploit non-pathology shortcuts such as source-specific text markers or positioning, and external validation alone does not prove clinical relevance.

### Cited Findings
- NIH labels were claimed over 90% accurate, but Oakden-Rayner's visual review of about 700 images found positive predictive values mostly 10-30% lower than documented, plus hidden stratification. Figures for pneumonia vary by secondary source (30-40% vs about 60%), so treat them cautiously — [AuntMinnie](https://www.auntminnie.com/imaging-informatics/artificial-intelligence/article/15624523/study-public-image-datasets-may-have-qc-issues); [arXiv 2010.03975](https://arxiv.org/pdf/2010.03975).
- Label errors are consistent between train and test, so test metrics can overstate real performance — [relayed commentary](https://aqsalose.kapsi.fi/blog/link-radiologist-dataset.html) (secondary source).
- Google released radiologist-adjudicated labels for part of ChestX-ray14 (about 37,000 images across two datasets) usable for cleaner evaluation — [Google Research blog](https://research.google/blog/developing-deep-learning-models-for-chest-x-rays-with-adjudicated-image-labels/).
- Shortcut learning: COVID CXR models used dataset-specific text markers and patient positioning, failing at new hospitals. External validation alone doesn't guarantee medical relevance. Authors recommend auditing with saliency maps — [DeGrave et al., Nat Mach Intell 2021 (medRxiv)](https://www.medrxiv.org/content/10.1101/2020.09.13.20193565v2); [UW news](https://news.cs.washington.edu/2021/06/01/allen-school-researchers-discover-medical-ai-models-rely-on-shortcuts-that-could-lead-to-misdiagnosis-of-covid-19-and-other-diseases).
- MIMIC-CXR-JPG labels carry an uncertain (-1) code, and a radiologist-labeled test set exists for evaluating labelers — [PhysioNet](https://physionet.org/content/mimic-cxr-jpg/2.1.0/).

### Inferences
- Recommended practice (my synthesis; not individually sourced): patient-level splits only; choose per-class thresholds on a held-out validation set (Youden or target sensitivity), never on test; calibrate (temperature scaling or per-class isotonic) and report ECE; stratify metrics by view position (AP/PA), sex, age and device; test on a non-NIH site such as VinDr-CXR; treat uncertain labels as ignore-mask or soft labels; run Grad-CAM and check it highlights the lung or lesion instead of corners, text or devices; consider masking or cropping border text.
- Because RSNA and ChestX-Det derive from NIH images, do not count them as external validation.

### Gaps
- No sources fetched for CheXpert uncertainty-handling results (U-Ones/U-zeros), calibration papers (Guo et al. 2017), view-position or tube/line shortcut papers (e.g., Zech 2018 pneumonia site confound), or Grad-CAM limitations (Adebayo sanity checks). These are known to me but not verified this session; cite after checking.

## Regulatory and licensing implications for a public app

### Takeaway
Research-use dataset terms and research-only model licenses make a public or commercial app risky. Stanford and PadChest explicitly bar commercial use; MIMIC/VinDr/BRAX are credentialed under a PhysioNet license whose commercial terms I could not verify. Models trained on such data may carry the same restrictions.

### Cited Findings
- CheXpert Plus agreement: no commercial use, research only, no redistribution — [arXiv 2405.19538](https://arxiv.org/pdf/2405.19538).
- Stanford AIMI: free for non-commercial research; commercial use via a separate process — [AIMI](https://aimi.stanford.edu/shared-datasets).
- PadChest: cannot be sold; non-academic use approved case by case — [BIMCV](https://bimcv.cipf.es/?p=4923).
- PhysioNet credentialed data: DUA forbids sharing and re-identification and requires code sharing for publications — [PhysioNet MIMIC-CXR-JPG](https://physionet.org/content/mimic-cxr-jpg/2.1.0/).
- BiomedCLIP card: deployed use, commercial or otherwise, is out of scope — [HF](https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224). TorchXRayVision describes itself as researcher-focused and does not address clinical use — [GitHub](https://github.com/mlmed/torchxrayvision).

### Inferences
- A public app should be framed as an educational or research demo, not a diagnostic device, with a clear disclaimer; any diagnostic claim would likely trigger medical-device regulation (FDA/CE; not researched here).
- Safest path for a public app: train only on data with verified permissive terms (or with written permission), and keep restricted datasets only for private internal validation, never redistributing images or derived datasets.

### Gaps
- No FDA/EU MDR/SaMD guidance researched. Whether weights trained on restricted data are legally encumbered was not verified (legal advice needed). Exact PhysioNet 1.5.0 commercial language not read.
