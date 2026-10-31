# Free health knowledge sources and APIs for a RAG consumer health assistant (inventory)

Note: items marked [UNVERIFIED] come from background knowledge and were not confirmed against a fetched source this session. This is not legal advice.

## Consumer health content (MedlinePlus, CDC, NHS, WHO, USPSTF, PubMed/PMC, StatPearls, ADA, Cochrane)

### Takeaway
The safest redistributable consumer-content sources are MedlinePlus (free, attribution requested), CDC (US-government, largely public domain), and the commercially-usable subset of PMC OA. WHO text is non-commercial by default, StatPearls is CC BY-NC-ND, and NHS has extra syndication terms. Treat those as retrieve-and-link or get permission before using them in a possibly commercial app.

### Cited Findings
- MedlinePlus web service: free, no registration or licence, keyword search returning XML (English/Spanish); asks for no more than 85 requests/min/IP, caching 12-24h, `email` and `tool` params; credit MedlinePlus.gov, do not use its logo or imply endorsement; data updated Tue-Sat. — [MedlinePlus web services](https://medlineplus.gov/about/developers/webservices/)
- MedlinePlus complete topic set is available as bulk XML (health topic XML, zip, topic groups, DTD), published daily Tue-Sat; NLM says you are welcome to download and use them with attribution. Topic-page images are licensed stock and may not be reproduced or redistributed. — [MedlinePlus XML / copyright (search summary)](https://medlineplus.gov/xml.html), [copyright](https://medlineplus.gov/copyright.html)
- MedlinePlus Connect: separate service, asks <=100 requests/min/IP, cache 12-24h. — [MedlinePlus Connect technical](https://medlineplus.gov/connect/technical.html)
- No source explicitly stated the MedlinePlus XML is "public domain"; some text is from third-party publishers. — [MedlinePlus copyright FAQ](https://medlineplus.gov/faq/copyrightfaq.html)
- CDC Content Services/syndication: free, some features need registration (email, organisation, domain); CDC web content is generally US-government public domain (conference abstract, not a licence); syndicated use must not imply CDC endorsement; third-party images or materials may have own copyright. No formal API licence text found. — [CDC syndication on Digital.gov](https://digital.gov/2012/11/05/centers-for-disease-control-content-syndication), [CDC tools](https://tools.cdc.gov/)
- NHS website content: available under Open Government Licence, but additional NHS website/syndication terms of use apply to API/widget content (refresh rates, e.g. required update more often than every 24h for a subset), and some content categories are excluded from OGL ("content not licensed for re-use"). Current text of the syndication terms was not retrievable. — [NHS terms](https://www.nhs.uk/our-policies/terms-and-conditions/), [content not licensed for re-use](https://www.nhs.uk/our-policies/terms-and-conditions/content-not-licensed-for-re-use/)
- WHO publications: CC BY-NC-SA 3.0 IGO (non-commercial; commercial use needs WHO permission; no implied endorsement; adaptations need disclaimers and same licence). Some items CC BY. ICD/ICF/ICHI are CC BY-ND 3.0 IGO. — [WHO copyright](https://www.who.int/about/policies/publishing/copyright)
- USPSTF recommendations API: needs an API key (since 2021-03-01, via USPSTF/AHRQ support); vendors must reproduce USPSTF text verbatim and cite it. Terms-of-use page dated 2013-2015; no dedicated API agreement found. — [USPSTF API](https://www.uspreventiveservicestaskforce.org/apps/api.jsp), [AHRQ EPSS](https://epssdata.ahrq.gov/)
- PubMed/NCBI E-utilities: 3 requests/s/IP without key, 10/s per key; higher by contacting NCBI; one key per account. — [E-utilities docs](https://www.ncbi.nlm.nih.gov/books/NBK25497/)
- PMC Open Access Subset: three tiers (commercial use allowed: CC0, CC BY, CC BY-SA, CC BY-ND; non-commercial: CC BY-NC variants; "Other"). Bulk via AWS S3 (`s3://pmc-oa-opendata/`, anonymous, us-east-1, XML and text), FTP, OAI-PMH, OA web service, BioC. PMC says ad-hoc scraping/bulk retrieval outside sanctioned channels is prohibited. Per-article licence governs. — [PMC OA list](https://pmc.ncbi.nlm.nih.gov/tools/openftlist), [AWS registry](https://registry.opendata.aws/ncbi-pmc/), [PMC text mining](https://pmc.ncbi.nlm.nih.gov/tools/textmining/)
- NCBI publishes precomputed MedCPT embeddings of all PubMed articles on its FTP server (so no need to embed PubMed yourself). — [MedCPT-Article-Encoder](https://huggingface.co/ncbi/MedCPT-Article-Encoder)
- StatPearls on Bookshelf: pages state CC BY-NC-ND 4.0 (copyright StatPearls Publishing); StatPearls own site terms prohibit copying/redistribution. A third-party listing showing some chapters as CC BY is unconfirmed; check per article. — [Bookshelf figure page example](https://ncbi.nlm.nih.gov/books/NBK560662/figure/article-32174.image.f1), [StatPearls terms](https://www.statpearls.com/home/privacypolicy/)

### Inferences
- MedlinePlus + CDC + PMC (CC0/CC BY/CC BY-SA/CC BY-ND only) is the best core corpus for an app that could be monetised. Filter PMC by licence field in the metadata.
- CC BY-ND (StatPearls, some PMC) prohibits derivatives; chunking/summarising into a vector store and LLM answers arguably touches this, so use retrieval for internal grounding with citation-and-link output rather than republishing text. Needs legal review.
- For NHS/WHO, use as linked references or ask permission; do not bulk-ingest if the app is commercial.

### Gaps
- Europe PMC (REST API; OA subset mirrors PMC licences) — not fetched this session [UNVERIFIED].
- ADA Standards of Care: not verified; my understanding is the summary is free to read in Diabetes Care but copyrighted, no open licence [UNVERIFIED].
- Cochrane: abstracts/plain-language summaries are free to read; full reviews mostly paywalled except open-access ones; reuse licence not verified [UNVERIFIED].
- NIH/NIDDK/NHLBI page reuse: US-government content, expected public domain, not verified.
- Current NHS syndication terms and API access process not retrievable.

## Drugs (openFDA, DailyMed, RxNorm/RxNav, DrugBank, interactions, India CDSCO)

### Takeaway
openFDA, DailyMed and RxNorm/RxNav are free and suited to a drug-lookup feature; DrugBank is non-commercial only. RxNav's own interaction API was discontinued, so interactions need another open source.

### Cited Findings
- openFDA limits: no key 240 req/min and 1,000 req/day per IP; with key 240 req/min and 120,000 req/day per key. — [openFDA authentication](https://open.fda.gov/apis/authentication/)
- DailyMed: RESTful web services (GET only) under dailymed.nlm.nih.gov/dailymed/services/, and bulk SPL zip downloads (full, daily, weekly, monthly), plus SPL-to-RxNorm mapping files (rxnorm_mappings.zip). — [DailyMed app support](https://dailymed.nlm.nih.gov/dailymed/app-support-web-services.cfm), [mapping files](https://dailymed.nlm.nih.gov/dailymed/app-support-mapping-files.cfm)
- RxNav APIs (RxNorm, RxTerms, Prescribable RxNorm, RxClass): no licence needed except the `/proprietary` function (needs UMLS); 20 requests/s/IP; cache 12-24h; RxNav-in-a-Box (Docker) for heavy use, governed by UMLS licence; RxNav drug-drug interaction API discontinued 2 Jan 2024. — [RxNav terms of service](https://lhncbc.nlm.nih.gov/RxNav/TermsofService.html), [FAQ](https://lhncbc.nlm.nih.gov/RxNav/information/FAQs.html)
- DrugBank: free academic/non-commercial only; downloads CC BY-NC 4.0; commercial use requires paid licence; some CC0 cross-reference datasets; academic downloads were temporarily paused at times. — [DrugBank terms](https://trust.drugbank.com/drugbank-trust-center/terms-of-use), [DrugBank FAQ](https://www.drugbank.ca/faqs)

### Inferences
- Use DailyMed SPL (bulk) for label text (indications, warnings, interactions section) and RxNorm for name normalisation (incl. Indian brand to generic via manual map). Avoid DrugBank for a commercial app.
- US labels are US-approved products; Indian brands/regulations differ, so show a disclaimer.

### Gaps
- openFDA/DailyMed formal reuse licence text (openFDA states data is public domain/CC0 in my memory) — not verified [UNVERIFIED]. Note openFDA data has accuracy disclaimers; adverse events are unverified reports.
- Open drug-interaction alternatives (DDInter, OpenFDA label sections, NIH DailyMed interaction text, TWOSIDES/SIDER, Drug Repurposing Hub): DDInter licence could not be confirmed (search returned nothing); SIDER is CC BY-NC-SA [UNVERIFIED].
- India CDSCO: no usable open API/dataset found or searched; I'd expect only PDF/portal listings [UNVERIFIED].

## Nutrition (USDA FDC, Open Food Facts, IFCT, WHO/FAO, ODS DRIs)

### Takeaway
USDA FoodData Central is the clean, CC0 backbone; Open Food Facts is useful for packaged goods (ODbL share-alike risk); IFCT 2017 is the right Indian reference but has no clear open licence.

### Cited Findings
- FDC: data CC0 1.0 public domain; credit requested; API key (data.gov) required; default 1,000 requests/hour/IP, exceeding blocks key 1 hour (HTTP 429); DEMO_KEY 30/hour, 50/day; data types Foundation, SR Legacy, FNDDS, Branded, Experimental; bulk CSV/JSON on Data Downloads page. — [FDC API guide](http://fdc.nal.usda.gov/api-guide/)
- Open Food Facts: ODbL database licence (attribution + share-alike; combined databases must be open), contents under Database Contents Licence; rate limits e.g. 100 req/min for product reads, per-user limit if called from mobile app, IP bans possible, custom User-Agent required. India coverage not verified. — [OFF API docs](https://openfoodfacts.github.io/openfoodfacts-server/api/), [OFF API conditions](https://support.openfoodfacts.org/help/en-gb/12-api-data-reuse/94-are-there-conditions-to-use-the-api)
- IFCT 2017 (NIN/ICMR): book copyright NIN; 528 key foods, 151 components; no composite dishes; no open licence found; community GitHub project (code AGPL-3.0 since May 2025, earlier MIT) packages the data. — [NIN IFCT2017 PDF](https://nin.res.in/ebooks/IFCT2017.pdf), [ifct2017 GitHub](https://github.com/ifct2017/ifct2017.github.io)

### Inferences
- ODbL share-alike applies to a derived database; querying OFF live with attribution is lower risk than merging into your own DB.
- Seek written permission from NIN before shipping IFCT values in the app; the AGPL wrapper does not clear data rights.

### Gaps
- NIH ODS DRI reference values (US NASEM/ODS fact sheets, public-domain NIH text expected) and WHO/FAO reference nutrient intakes: not fetched [UNVERIFIED]. ICMR-NIN 2020 RDAs for Indians are the more relevant source; availability/licence not checked.
- FDC full download sizes not retrieved.

## Terminologies (LOINC, SNOMED CT, UMLS, ICD-11)

### Takeaway
Terminologies are mostly unnecessary for a consumer RAG assistant; if needed, ICD-11 (CC BY-ND, commercial OK, no adaptations) and LOINC (free with accepted terms) are easiest; SNOMED CT and UMLS carry licence/territory constraints.

### Cited Findings
- UMLS licence: no NLM fees; bars distribution of the Metathesaurus or subsets except inside applications built for other purposes; Category 3 sources limited to internal use; Category 4 sources restricted to US use/distribution; separate agreements with copyright holders may apply. Which sources are in which category is on a separate list not read. — [UMLS licence](https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/license_agreement.html)
- LOINC: free worldwide, must accept terms of use at download; redistribution terms not retrieved. — [OHDSI forum on licensing](https://forums.ohdsi.org/t/licensing-terms-for-vocabulary-download/19628)
- SNOMED CT: Affiliate Licence via National Release Centre or SNOMED International; may incur fees in non-member countries. India membership not confirmed. — [SNOMED LOINC guide](https://docs.snomed.org/implementation-guides/loinc-implementation-guide/technical-application/6.2-accessing-the-loinc-ontology)
- ICD-11: CC BY-ND 3.0 IGO (commercial and non-commercial use; no adaptations); API hosted by WHO, plus local Docker/Windows/Linux deployment. Hosted API rate limits/quotas not found. — [ICD-11 licence](https://icd.who.int/icdapi/docs2/license), [ICD-API](https://icd.who.int/icdapi)

### Inferences
- Use MedlinePlus topic names/ICD-10 or ICD-11 links for coding; skip SNOMED CT/UMLS unless needed.

### Gaps
- India SNOMED CT status; LOINC redistribution detail; ICD-11 API quotas.

## RAG practicalities (embeddings, rerankers, vector stores, repos, evaluation)

### Takeaway
MedRAG/MIRAGE provide a ready benchmark and evidence that MedCPT retrieval on PubMed/textbooks helps; most models and vector stores listed are open-source, but licences must be confirmed per model card.

### Cited Findings
- MedRAG toolkit: corpora PubMed, StatPearls, textbooks, Wikipedia; retrievers BM25, Contriever, SPECTER, MedCPT (~109M params); MIRAGE = 7,663 questions from five medical QA datasets; reports up to 18% accuracy gain on six LLMs over CoT; precomputed embeddings available; needs Java for BM25. Licence file not read. — [MedRAG GitHub](https://github.com/Teddy-XiongGZ/MedRAG)
- MedCPT encoders (NCBI): HF licence tag "other / public-domain" with separate LICENSE file; paper arXiv 2307.00589. — [MedCPT-Article-Encoder](https://huggingface.co/ncbi/MedCPT-Article-Encoder)

### Inferences
- MedRAG's StatPearls corpus is CC BY-NC-ND; do not copy that corpus into a commercial product.
- Reasonable stack: MedCPT or a general model (bge-m3 / e5) + hybrid BM25 + reranker (e.g. bge-reranker or MedCPT Cross-Encoder), stored in Supabase pgvector (pgvector + Postgres full text) for simplicity.

### Gaps
- Licences for BGE (I recall MIT), e5 (MIT), BiomedBERT/PubMedBERT (MIT), Chroma (Apache-2.0), Qdrant (Apache-2.0), pgvector (PostgreSQL licence), RAGAS (Apache-2.0): all [UNVERIFIED], recalled from memory.
- Supabase free-tier limits (database size, e.g. 500 MB) not verified; Qdrant Cloud free tier size not verified.
- Other open medical RAG repos and benchmarks (e.g. HealthBench, MedQA, PubMedQA) not searched.
