# Free/open knowledge sources for symptom checking, triage, and mental-health screening (as of Oct 2026)

Verification legend: items in "Cited Findings" were seen in a fetched or search-returned source this session. Items marked UNVERIFIED are from background knowledge only and must be checked before reliance. Many search results were secondary sources, and this is noted where relevant.

## Symptom/disease knowledge sources (Orphadata, HPO, DO, SNOMED, UMLS, ICD, MedlinePlus)

### Takeaway
Best license-clear backbone for a symptom-to-condition knowledge layer: HPO plus Orphadata annotations (rare disease, free), MedlinePlus Connect (free consumer-text API, 100 req/min), and ICD-11 API (free with registration). SNOMED CT and UMLS are free only under the NLM/UMLS affiliate license, per-user, with territory conditions. None of these is a triage protocol, so they cover knowledge and coding, not urgency.

### Cited Findings
- Orphadata datasets are described (by a downstream project, not Orphadata's own page) as downloadable under CC BY 4.0 with attribution, commercial use allowed. Verify on orphadata.com. — [search result summary](https://www162.lamp.le.ac.uk/vocabularies/ordo)
- HPO disease-phenotype annotations are described as freely available, and the HPO disease annotation corpus is available at Orphadata.org. One record said license restrictions apply to HPO-provided files, so exact terms were not confirmed. The hpo.jax.org/license URL returned 404. — [HPO paper (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4572507/); [HPO terminology record](https://terminology.art-decor.org/codesystems/terminology-stable-hpo-data); [HPO 2024 NAR paper](https://core.ac.uk/works/154459837)
- SNOMED CT: NLM distributes it free in the US and other IHTSDO Member territories, via the UMLS Metathesaurus License, Appendix 2 (SNOMED CT Affiliate License). It is free in Member territories, low-income countries, and for qualifying research. Each downloader needs their own license, and there are no organizational or enterprise licenses. Use in non-Member countries requires notifying and registering with IHTSDO, and fees may apply. The page does not mention India. India's membership status is a gap. — [NLM SNOMED licensing](https://www.nlm.nih.gov/healthit/snomedct/snomed_licensing.html)
- ICD API (WHO): registration is required to get an access key. Docker, Windows-service, or systemd local installs are available. The Embedded Classification Tool (v1.8) is powered by the API. The page says the "ICD-11 License is now more open", but the exact license (CC BY-ND 3.0 IGO is my recollection, UNVERIFIED) and rate limits were not confirmed. — [WHO ICD API](https://icd.who.int/icdapi)
- MedlinePlus Connect: base `https://connect.medlineplus.gov/service`, HTTPS only, HL7 Infobutton parameters, XML Atom default, JSON via `knowledgeResponseType=application/json`. It supports ICD-10-CM, ICD-9-CM, and SNOMED CT for diagnoses, plus RxCUI/NDC, LOINC, and CPT. Spanish is available with `informationRecipient.languageCode.c=es`. The limit is 100 requests/min per IP, with a 300 s block when exceeded, and caching for 12-24 h is recommended. You may link to and display the data, but not copy pages wholesale. Credit MedlinePlus.gov and do not imply endorsement. The XML health-topic files are the bulk alternative. — [MedlinePlus Connect docs](https://medlineplus.gov/connect/service.html)
- Not verified this session (background knowledge, check before use): Disease Ontology is CC0, UMLS requires a free UTS account and license acceptance, HPO annotation file is `phenotype.hpoa`, and Orphadata offers a free XML/JSON product set (en_product4 = HPO phenotypes of rare diseases).

### Inferences
- A rule or knowledge layer built on HPO/Orphanet is biased toward rare diseases, and common conditions need other sources (MedlinePlus text, ICD codes).
- For an India-based project, SNOMED CT licensing depends on India's IHTSDO/SNOMED International membership, which must be confirmed. ICD-10/11 plus MedlinePlus avoids that issue.

### Gaps
- Exact HPO license text, the Orphadata license page, and ICD-11 license terms were not retrieved.
- NHS conditions/symptom content (the NHS Website API) was not checked.

## Symptom-to-disease datasets, open triage protocols, vignette and QA benchmarks

### Takeaway
Kaggle symptom-disease tables are small and unreliable for real triage. Open triage protocols were not found: Schmitt-Thompson is licensed, and the GitHub symptom checkers surfaced are prototypes. For evaluation, use MedQA, MedMCQA, PubMedQA, and Semigran-style vignettes (45 cases), noting that these test knowledge and diagnosis, not safe triage behavior.

### Cited Findings
- Kaggle "41-disease" dataset: about 4,920 records and 132 symptom columns, with disease count reported as 41 or 42. A student project's model could predict only 12 of 41 diseases. Papers report 98-100% accuracy, which suggests that the data is artificially clean. No source confirmed it is synthetic, so check the dataset card. — [arXiv 2302.12075](https://arxiv.org/pdf/2302.12075); [Temple project PPT](https://cis.temple.edu/~pwang/5603-AI/Project/2022S/pateljanvi/Final_Project_PPT.pdf)
- Symptom2Disease: 1,200 datapoints, 24 diseases, 50 free-text symptom descriptions each. — [arXiv 2502.07755](https://arxiv.org/pdf/2502.07755)
- Semigran et al., BMJ 2015: 23 symptom checkers, 45 vignettes (15 emergency, 15 non-emergency, 15 self-care, per secondary sources). Aggregate triage accuracy was about 57%, and advice was risk-averse. A 2020 re-test found similar median triage accuracy (55.8% vs 59.1%). Vignette text availability in the appendix (doi 10.1136/bmj.h3480) was not confirmed. — [Semigran-related BMJ page](https://www.bmj.com/node/900623); [JMIR 2022 e31810](https://www.jmir.org/2022/5/e31810)
- MedQA-USMLE-4-options (HF, GBaker): CC-BY-4.0, 10.2k train and 1.27k test (11,451 rows). — [HF](https://huggingface.co/datasets/GBaker/MedQA-USMLE-4-options)
- PubMedQA: MIT on HF, with pqa_labeled ~1k, pqa_artificial ~211k, pqa_unlabeled ~61.2k. — [HF](https://huggingface.co/datasets/qiaojin/PubMedQA)
- MedMCQA: about 194k AIIMS/NEET-PG questions across 21 subjects, listed as Apache-2.0 in an older HF loading script (recheck the current card). Relevant to Indian exam context. — [TFDS catalog](https://www.tensorflow.org/datasets/community_catalog/huggingface/medmcqa?hl=fr)
- MultiMedQA = MedQA + MedMCQA + PubMedQA + LiveQA + MedicationQA + MMLU clinical topics, plus the new HealthSearchQA of commonly searched health queries. The paper gives no license. — [Singhal et al.](https://arxiv.org/pdf/2212.13138)
- Open-source repos found (all small, prototype-grade, maintenance not verified): LabinatorSolutions/medical-symptom-checker (GPLv3, no visible clinical validation) — [GitHub](https://github.com/LabinatorSolutions/medical-symptom-checker); emdmed/triageapi (urgency score, Buenos Aires only) — [GitHub](https://github.com/emdmed/triageapi); prak112/ICD11-SymptomChecker (non-commercial license, uses ICD-11 API) — [GitHub](https://github.com/prak112/ICD11-SymptomChecker); AY-Khalid/DocAgent (LLM triage, author says demo only) — [GitHub](https://github.com/AY-Khalid/DocAgent).
- Infermedica requires an API key by registration; commercial terms were not found. — [API directory listing](https://public-api.org/api/838/infermedica)
- Background knowledge, UNVERIFIED: Schmitt-Thompson protocols are proprietary. NHS Pathways is licensed through NHS England/NHS Digital. HealthSearchQA availability on public hosting needs checking. Known weakness of Semigran-style evaluation: small N, and a vignette's expected triage level is the authors' judgment.

### Inferences
- No clinically validated, permissively licensed, open triage rule set was found. A pragmatic design is a conservative red-flag layer written and reviewed by clinicians, using public guidance (for example NHS or WHO IMCI-type guidance, UNVERIFIED), with LLM output constrained to "seek care" levels.
- MedQA/MedMCQA/PubMedQA measure exam knowledge. A custom vignette set with expected triage level is needed to test safety, with over-triage and under-triage scored separately.

### Gaps
- No open-license NHS 111 / Pathways data found. Infermedica terms, current maintenance of the GitHub repos, and the HealthSearchQA and MultiMedQA licenses are unverified.

## Mental-health screening instruments: licensing, scoring, translations, crisis and safe messaging

### Takeaway
PHQ-9 and GAD-7 are explicitly free to use (Pfizer, 2010), and phqscreeners.com carries a Hindi version. AUDIT is described as public domain (conflicting with an NHS listing), and EPDS is free with acknowledgment. PCL-5 is widely treated as public domain with a provisional 31-33 cutoff. ASRS terms were not verified. Screening scores must be framed as screening, not diagnosis, with crisis routing for PHQ-9 item 9.

### Cited Findings
- PHQ-9/GAD-7 released without copyright restriction or charge by Pfizer in 2010. The developer site states they are public domain, with no permission needed to reproduce, translate, display, or distribute, and offers translations in nearly 80 languages. The statement quoted comes from a 2012 archive through CamCOPS, so recheck the live site. phqscreeners.com lists terms, a public domain statement, instruments, a Hindi translation, and scoring instructions. — [phqscreeners.com](https://www.phqscreeners.com/); [CamCOPS GAD-7](https://camcops.readthedocs.io/en/latest/tasks/gad7.html); [FiercePharma](https://www.fiercepharma.com/pharma/pfizer-to-offer-free-public-access-to-mental-health-assessment-tools-to-improve-diagnosis)
- A 2021 paper (Zorowitz et al.) reported a GAD-7 item reproduction error in some copies. Copy wording only from the official source. — [CamCOPS](https://camcops.readthedocs.io/en/latest/tasks/gad7.html)
- Hindi PHQ-9 validation exists only for specific populations: leprosy patients in Jharkhand (alpha 0.81), cancer palliative care (cultural adaptation, two-factor model), and head-and-neck cancer (reliability 0.717-0.890 across Tamil, Telugu, Hindi). No standardized national general-population validation was found. — [VU thesis record](https://infontd.org/media/1391/download); [IJPC adaptation](https://jpalliativecare.com/?p=7068); [J Patient Rep Outcomes 2021](https://doaj.org/article/234fedd6d5c946eeab0c17b2357147b6)
- PCL-5: ISTSS states the 31-33 cutoff (Bovin et al. 2016) for probable PTSD, with studies ranging 28-37. Public-domain status came only from vendor sites, so verify at ptsd.va.gov. Vendor sites say no official severity bands exist. — [ISTSS](https://istss.org/Clinical-Resources/Assessing-Trauma/PTSD-Checklist-DSM-5)
- AUDIT: AUDIT FAQ site says it is public domain as a WHO-approved instrument. NHS NCCR lists it as free but with commercial restrictions, so these conflict. — [AUDIT FAQ](https://auditscreen.org/about/faqs/); [NHS NCCR](https://digital.nhs.uk/services/national-clinical-content-repository-copyright-licensing-service/nccr-tools-and-measures-library)
- EPDS: authors permit free reproduction with copyright acknowledgment, and copyright is held by the British Journal of Psychiatry. The NHS repository lists it as licensed, so terms may differ. — [Scottish NHS toolkit](https://www.rightdecisions.scot.nhs.uk/mental-health-in-pregnancy-and-after-birth-sign-169/recommendations-for-health-and-social-care-professionals/questionnaires-and-scoring-tools/)
- Open implementation: CamCOPS (open-source task library with PHQ-9, GAD-7 docs). Its license and maintenance were not checked. — [CamCOPS PHQ-9](https://camcops.readthedocs.io/en/latest/tasks/phq9.html)
- India crisis: Tele-MANAS, 14416 or 1800-891-4416, 24/7, launched 10 Oct 2022, run by MoHFW, about 20 languages. KIRAN (1800-599-0019) was merged into Tele-MANAS from Feb 2024 and some directories still list it. — [Vikaspedia](https://en.vikaspedia.in/viewcontent/health/mental-health/national-tele-mental-health-programme?lgn=en); [BioSpectrum](https://biospectrumindia.com/news/98/24217/govt-merges-kiran-mental-health-rehabilitation-helpline-with-telemanas.html)
- US: 988 Lifeline offers 24/7 call, text, and chat in English and Spanish. A GAO report (GAO-26-108114) says text volume grew about 260% and calls about 87% through Sept 2025. — [988lifeline.org FAQ](https://988lifeline.org/faq/); [GAO-26-108114](https://www.gao.gov/products/GAO-26-108114)
- Findahelpline.com (run by ThroughLine) claims verified helplines in 175+ countries. No public API or terms were visible, and developer access likely goes via ThroughLine's integrations/partnership route (unconfirmed). — [findahelpline.com](https://findahelpline.com/)
- Safe messaging: a systematic comparison found guidelines agree on avoiding method details and encouraging help-seeking, and that terminology is contested. A RAND-led study found chatbots refuse high-risk how-to queries but handle medium-risk ones inconsistently. A JMIR 2026 study warns that UI safety does not necessarily generalize to API-built apps. Multi-turn behavior is under-studied. — [suicideinfo.ca](https://www.suicideinfo.ca/?p=154203); [JMIR 2026 e97968](https://www.jmir.org/2026/1/e97968); [AI and Suicide Prevention primer](https://arxiv.org/pdf/2605.04321)
- UNVERIFIED background knowledge, fetch the official sources before coding thresholds: PHQ-9 total 0-27 with bands 5/10/15/20 (mild, moderate, moderately severe, severe) and a >=10 screening cutoff. GAD-7 total 0-21 with bands 5/10/15 and a >=10 cutoff. AUDIT total 0-40, with 8+ indicating hazardous use. EPDS total 0-30, commonly using 10 or 13 as cutoffs, and item 10 asks about self-harm. ASRS v1.1 Part A has 6 items with a shaded-box rule, but its WHO copyright and permission terms were not found.

### Inferences
- Item 9 of PHQ-9 and EPDS item 10 should trigger the crisis branch regardless of total score.
- Hindi PHQ-9 can be shipped from the official site, but it should be described as a translation with limited validation, not as validated for the general Indian population.
- Region-aware crisis routing needs a maintained table (Tele-MANAS 14416, 988, etc.), with findahelpline.com as a fallback pointer for other countries, pending its terms.

### Gaps
- Current live license text of phqscreeners.com, ptsd.va.gov PCL-5 terms, ASRS permission, EPDS cutoffs, and AFSP/WHO/reportingonsuicide.org guideline content were not retrieved. Hindi versions of GAD-7, PCL-5, ASRS, AUDIT, and EPDS were not checked. Other regional hotlines (UK Samaritans 116 123 etc.) are unverified.

## Open mental-health text datasets and why they must not be used for diagnosis

### Takeaway
The accessible sets are GoEmotions (Apache-2.0), Dreaddit, and the gated ones (DAIC-WOZ, SWMH, CLPsych) that need signed agreements. All are proxies: labels are crowd, subreddit, or keyword based, not clinical, so models trained on them should not diagnose.

### Cited Findings
- GoEmotions: Apache-2.0, about 58k Reddit comments, 27 emotions plus neutral (simplified split 43,410 / 5,426 / 5,427). Annotated by three crowdworkers in India. Authors warn of Reddit-user, filtering, and annotator biases, and the data contains usernames. It is an emotion dataset, not a clinical one. — [HF](https://huggingface.co/datasets/google-research-datasets/go_emotions)
- DAIC-WOZ: access via application form and EULA from USC ICT. The extended DAIC version (AVEC 2019) is also on request. — [USC ICT](https://dcapswoz.ict.usc.edu/); [EULA form](https://form.jotform.com/220456805306149)
- DAIC-WOZ weaknesses: therapist prompts leak signal, and interviewer effects exist. — [arXiv 2404.14463](https://arxiv.org/pdf/2404.14463); [arXiv 2603.24651](https://arxiv.org/pdf/2603.24651)
- SWMH: Zenodo restricted record, institutional email and Data Access Agreement required, no redistribution, research use only, password-protected storage. — [Zenodo](https://zenodo.org/record/6476179) and [benchmark suite arXiv 2604.23458](https://arxiv.org/pdf/2604.23458)
- CLPsych 2015 data requires a signed agreement and confidentiality, with use limited to the shared task in one report. Dreaddit is a stress dataset that is easier to obtain, and one survey mislabels it for suicide risk. — [EMNLP 2020 repo](https://github.com/kharrigian/emnlp-2020-mental-health-generalization); [MentalBERT](https://arxiv.org/pdf/2110.15621)

### Inferences
- Labels from subreddit membership or self-declared diagnosis capture community language, not diagnosis. Performance does not generalize across platforms and populations (the topic of the EMNLP 2020 generalization repo), and the data carries demographic bias and privacy risk.
- Use these data only for research on emotion or language understanding, tone testing, and red-team prompt sets. Do not use them for diagnostic claims, and use validated instruments with clinician follow-up for any assessment.

### Gaps
- GoEmotions-like open datasets with explicit clinical labels were not found. Licensing of Dreaddit and the UMD suicidality dataset was not verified. The Hugging Face connector was unauthorized and not used.
