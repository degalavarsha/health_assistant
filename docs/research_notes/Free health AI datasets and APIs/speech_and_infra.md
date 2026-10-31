# Speech recognition, medical term handling, and free-tier infrastructure for a consumer health assistant

Research date: 2026-10-31. Items marked UNVERIFIED come from memory or secondary sources and were not confirmed on a primary page in this session.

## ASR options (CPU-friendly) and Indian-language support

### Takeaway
For CPU/free-tier use, faster-whisper (MIT) with small or int8-quantised larger Whisper models is the practical default for English. Hindi is workable with Indic-tuned models (IndicWhisper about 13.6% average WER on Vistaar). Telugu and other Dravidian languages are clearly harder (IndicWhisper about 28.8% average WER). Parakeet v3 and Moonshine do not cover Indian languages in the sources checked. Voice input for numbers should always be confirmed by the user.

### Cited Findings
- faster-whisper is MIT-licensed. Small model, int8, beam 5, 8 threads on an i7-12700K took 1m42s using 1477 MB RAM. Batched (batch_size 8) took 51s using 3608 MB. The same benchmark shows openai/whisper fp32 at 6m58s and whisper.cpp fp32 at 2m05s. The README gives no CPU numbers for large-v3, turbo or distil. — [faster-whisper README](https://github.com/SYSTRAN/faster-whisper)
- faster-whisper states Distil-Whisper checkpoints (e.g. distil-large-v3) are compatible. — [faster-whisper README](https://github.com/SYSTRAN/faster-whisper)
- whisper.cpp is MIT-licensed, pure C/C++, CPU-only capable (AVX, NEON, OpenBLAS), supports integer quantisation. Memory: tiny about 273 MB, base about 388 MB, small about 852 MB, medium about 2.1 GB, large about 3.9 GB. — [whisper.cpp README](https://github.com/ggml-org/whisper.cpp)
- Whisper large-v3-turbo: about 809M parameters vs 1,550M for large-v3 (decoder cut from 32 to 4 layers), "way faster" with "minor quality degradation", MIT licence. The card warns Whisper performs unevenly across languages, with worse accuracy and more hallucination/repetition in low-resource languages. — [whisper-large-v3-turbo card](https://huggingface.co/openai/whisper-large-v3-turbo)
- Open ASR Leaderboard blog (long-form): Whisper Large v3 WER 6.43 / RTFx 68.56; Parakeet CTC 1.1B WER 6.68 / RTFx 2793.75 but English-only. Distil-Whisper (distil-large-v3.5) often beats the original on English-only tasks (no figures). — [HF Open ASR leaderboard blog](https://huggingface.co/blog/open-asr-leaderboard)
- NVIDIA Parakeet-TDT-0.6B-v3: 0.6B params, CC BY 4.0, commercial use allowed, needs at least 2 GB RAM, supports 25 European languages only (no Hindi/Telugu listed). Leaderboard average WER 6.34%; Fleurs multilingual average 11.97%; degrades in noise (11.66% at 0 dB SNR, 19.88% at -5 dB). — [Parakeet v3 card](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3)
- Moonshine: library MIT; models MIT except legacy non-English non-streaming models, which use a non-commercial Moonshine Community License. Targets low-latency on-device streaming; the README does not list languages or give CPU/WER numbers. — [Moonshine README](https://github.com/moonshine-ai/moonshine)
- Vosk (Apache 2.0) Indian models: vosk-model-small-hi-0.22 (42 MB; WER 20.89 IITM, 24.72 MUCS), vosk-model-hi-0.22 (1.5 GB; 14.85 CV, 14.83 IITM, 13.11 MUCS), vosk-model-small-te-0.42 (58 MB; 87.9 on Fleurs, i.e. effectively unusable). — [Vosk models](https://alphacephei.com/vosk/models)
- AI4Bharat IndicWhisper (Vistaar benchmark, 12 languages, trained on about 10.7K hours public data): lowest WER on 39 of 59 benchmarks. Average WER by language: Hindi 13.6, Telugu 28.8, Tamil 25.3, Kannada 18.3, Marathi 18.2, Bengali 20.1, Malayalam 32.3, Gujarati 22.8, Punjabi 20.5, Urdu 19.4, Odia 27.4, Sanskrit 48.0. Hindi comparison: Nvidia-large 18.6, Azure 20.0, IndicWav2vec 21.0, Google STT 23.9. Repo and fine-tuned checkpoints are MIT (per-language zip files; Whisper-sized models, so CPU speed is that of the base Whisper size used). — [Vistaar/IndicWhisper repo](https://github.com/AI4Bharat/vistaar); paper [arXiv 2305.15386](https://arxiv.org/abs/2305.15386)
- AI4Bharat IndicConformer 600M (MIT): 22 Indian languages, hybrid CTC+RNNT, Hindi WER 13.2 on Vaani benchmark; model page recommends a newer Indic-Transcribe model (25 languages) and gating requires sharing HF info. — [IndicConformer card](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual)

### Inferences
- A CPU-only free host with about 2 vCPU/16 GB RAM (e.g. HF CPU Basic) can run faster-whisper small/base int8 in near real time for short clips; large-class models are likely too slow for interactive use without GPU (inference from the small-model benchmark; no direct large-v3 CPU benchmark was found).
- For Indian languages, options are: IndicWhisper (best published Hindi), IndicConformer (22 languages, 600M, CPU feasible but heavier), or generic Whisper (unverified accuracy on Hindi/Telugu). Telugu quality (about 29% WER even for the best Indic-tuned Whisper) is too low to trust for medical numbers without confirmation.
- Parakeet v3 and Vosk-Telugu are poor fits for Indian-language medical voice input.

### Gaps
- No primary-source CPU latency numbers for large-v3, turbo, distil on CPU, or for IndicWhisper/IndicConformer on CPU.
- Whisper large-v3 / turbo WER on Hindi and Telugu (Fleurs/Common Voice) not retrieved. UNVERIFIED: commonly cited as much worse than IndicWhisper for Telugu.
- Distil-Whisper licence (believed MIT) and Canary (believed CC BY-NC for older Canary-1B; Canary-Qwen licence) not verified. Moonshine supported-language list not retrieved.
- Indic-Transcribe model details/licence not checked.

## Medical speech datasets and medical term handling

### Takeaway
Open medical ASR data is small and mostly English/European/Chinese; there is no verified open Hindi/Telugu medical speech corpus from this search. Practical term handling = Whisper prompt biasing (limited to about 224 tokens) plus fuzzy post-correction against a drug/term lexicon plus LLM correction constrained to the lexicon, with explicit user confirmation for numbers and drug names.

### Cited Findings
- MultiMed: about 150 hours, 5 languages (Vietnamese, English, French, German, Mandarin), real medical conversations from YouTube medical channels, ACL 2025 industry paper; HF dataset card (copy) lists MIT licence, but the paper page did not state a data licence (the CC BY label refers to the paper). Hours are English about 84 h, others about 5 to 8 h. Whisper-medium decoder-only fine-tune test WER: English 19.41, Vietnamese 25.43, French 31.05, German 17.92; Chinese is CER (small model) 34.28. Common errors: wrong drug names and dosages, left/right confusion, dates. — [MultiMed arXiv](https://arxiv.org/html/2409.14074v3); [HF card copy](https://huggingface.co/datasets/ttthe/MultiMed/blob/main/README.md)
- PriMock57: 57 mock primary care consultations with ASR evaluation (arXiv 2204.00333). Licence not found in search. — [PriMock57 paper](https://arxiv.org/pdf/2204.00333)
- Rare-word biasing study: Whisper prompt window is about 224 tokens (about 70 words); rare-word recognition worsens as the biasing list grows; prompt biasing helped English but transferred poorly to French and German with the base model. — [arXiv 2502.11572](https://arxiv.org/pdf/2502.11572)
- Zero-shot Whisper performed poorly on single-word clinical speech from an unseen dataset; fine-tuning cut WER substantially (post-stroke naming study). — [NeurIPS 2025 workshop](https://neurips.cc/virtual/2025/124949)
- Prompt-tuning Whisper improved robustness to unseen medical terms, though overall WER stayed high. — [arXiv 2605.05231](https://arxiv.org/pdf/2605.05231)

### Inferences
- Because documented medical ASR errors include wrong drug names, dosages and left/right, any extracted number/unit/drug must be shown back to the user (text and optionally read aloud) and require confirmation before being stored or used.
- Prompt biasing should use a short, context-specific list (e.g. 20 to 40 terms for the current screen) rather than a large lexicon, to avoid over-biasing.
- Fuzzy matching (e.g. edit distance/phonetic) against a closed lexicon (RxNorm/drug list/local brand names) is cheap on CPU and testable; LLM correction should only choose among lexicon candidates, not invent terms.

### Gaps
- Did not verify "Medical Speech Transcription" sets on Hugging Face, MedDG (that is a text dialogue dataset, not speech), PriMock57 licence/hosting, or any Indian-language medical speech data (e.g. Hindi clinical speech). Treat as not found.
- No quantified benchmark for fuzzy or LLM post-correction on medical ASR was retrieved.

## Number/unit extraction and clinical NER

### Takeaway
For vitals and doses (e.g. BP 120/80, glucose 140 mg/dL, 500 mg), deterministic regex plus unit normalisation and range checks is the safest base layer. NER or LLM structured output helps for free-form phrasing and entities (drug, symptom), with licences all permissive for the software.

### Cited Findings
- scispaCy: Apache-2.0 software; models en_core_sci_sm/md/lg/scibert and NER models for CRAFT, JNLPBA, BC5CDR, BioNLP13CG (v0.5.4); UMLS linker covers about 3M concepts. The page does not state model-file licences or UMLS terms. — [scispaCy](https://github.com/allenai/scispacy)
- medspaCy: MIT, in beta; ConText (negation/uncertainty), section detection, QuickUMLS integration; English most complete. Latest listed release 1.3.1 (Nov 2024). — [medspaCy](https://github.com/medspacy/medspacy)
- GLiNER: Apache-2.0 zero-shot NER, fine-tunable to biomedical corpora; the repo page names no biomedical-specific models. — [GLiNER](https://github.com/urchade/GLiNER)

### Inferences
- Recommended hybrid: regex/grammar for numbers+units (plus spoken-number normalisation, including Hindi/Telugu number words), plausibility ranges, then an LLM or GLiNER only to tag what the number refers to; always confirm.
- scispaCy/medspaCy are English-centric and add UMLS data/licence obligations; likely overkill for a consumer app unless entity linking is needed.

### Gaps
- GLiNER-biomed model names and licences, scispaCy model licences, UMLS licence terms (UMLS requires a licence agreement, believed; UNVERIFIED), and accuracy numbers for regex vs NER vs LLM on spoken vitals were not found.

## Free-tier infrastructure (verified on official pages 2026-10-31)

### Takeaway
Best free fit for a prototype: Supabase (500 MB Postgres + auth + RLS, but pauses after 1 week inactivity and no backups) or Neon (1 GB/project, scale-to-zero, no pausing of data). Free compute hosts are limited: Render sleeps and its free Postgres expires after 30 days; Fly has no free tier; Hugging Face Gradio/Docker Spaces now need a paid plan; Vercel Hobby is non-commercial only. None of the free plans should hold real identifiable health data without a compliance review.

### Cited Findings
- Supabase Free: 500 MB database per project (shared CPU, 500 MB RAM), 1 GB file storage (50 MB max upload), 50,000 MAU, 2 active projects, projects paused after 1 week of inactivity, 5 GB egress, no automatic backups. — [Supabase pricing](https://supabase.com/pricing)
- Supabase pgvector: extension named `vector`, enabled via Dashboard Extensions or `create extension vector with schema extensions`; the page does not state plan availability (UNVERIFIED for Free; widely believed available). — [Supabase pgvector docs](https://supabase.com/docs/guides/database/extensions/pgvector)
- Supabase compliance: SOC 2 Type 2, ISO 27001, GDPR support (EU region, DPA), HIPAA via a HIPAA add-on; page does not specify which plans qualify. — [Supabase compliance](https://supabase.com/docs/guides/platform/compliance)
- Neon Free: permanent, no card; up to 100 projects; 1 GB storage per project (20 GB total); 100 CU-hours per project per month; compute suspends after 5 minutes idle (cannot be disabled); 5 GB egress; 10 branches; 6-hour history; Auth up to 60,000 MAU. Exceeding compute/egress suspends compute until next period; exceeding storage blocks writes; no data deleted. — [Neon pricing](https://neon.com/pricing)
- MongoDB Atlas M0: 0.5 GB storage (including indexes), max 500 connections, 100 ops/sec, 10 GB in/out per rolling 7 days, auto-paused after 30 days of inactivity, one free cluster per project, MongoDB 8.0, daily snapshots if enabled. Vector search limits not on this page (UNVERIFIED: Atlas Vector Search is believed available on M0 with a small index cap). — [Atlas free limits](https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/)
- Render Free web service: spins down after 15 min idle (about 1 minute to wake), 750 instance hours per workspace per month, ephemeral filesystem, no persistent disks. Free Postgres: 1 GB, one per workspace, expires after 30 days (14-day grace then deleted), no backups. — [Render free docs](https://render.com/docs/free)
- Fly.io: no free tier or monthly allowance for new orgs; trial of up to 2 hours machine runtime or 7 days; cheapest always-on machine (shared-cpu-1x 256 MB) $2.19 per 30 days plus egress. — [Fly pricing](https://docs.fly.io/about/pricing)
- Hugging Face Spaces: default CPU Basic is 2 vCPU/16 GB, free hardware sleeps when unused, but creating Gradio or Docker Spaces now requires a paid plan (PRO etc.); static Spaces are free; free accounts can host up to 2 Gradio Spaces on ZeroGPU. (The built-in env var example in the same doc lists 4 cores / 15 Gi, minor inconsistency.) — [HF Spaces overview](https://huggingface.co/docs/hub/spaces-overview)
- Vercel Hobby: free, non-commercial personal use only; 100 GB fast data transfer, 1M function invocations, 4 CPU-hours active CPU, function max duration 300 s, 100 deployments/day; exceeding limits blocks the feature for about 30 days. — [Vercel Hobby](https://vercel.com/docs/plans/hobby)
- Cloudflare Workers Free: 100,000 requests/day, 10 ms CPU per request, 128 MB memory, 50 subrequests. D1 Free: 5 GB storage, 5M rows read/day, 100k rows written/day, 10 databases. — [Workers limits](https://developers.cloudflare.com/workers/platform/limits/); [D1 pricing](https://developers.cloudflare.com/d1/platform/pricing/)
- India DPDP: Rules notified 13 Nov 2025; phased commencement; consent-manager provisions 13 Nov 2026; full obligations for data fiduciaries by 13 May 2027; SPDI Rules 2011 remain meanwhile. Reported proposals to accelerate for significant data fiduciaries were unconfirmed. — [Hogan Lovells](https://www.hoganlovells.com/en/publications/indias-digital-personal-data-protection-act-2023-brought-into-force-); [AZB](https://www.azbpartners.com/bank/indias-digital-personal-data-protection-act-phased-rollout-and-key-compliance-milestones/)

### Inferences
- Cloudflare Workers' 10 ms CPU and 128 MB make it unsuitable for running ASR, but fine as a proxy or static frontend host; Vercel Hobby also cannot be used for a commercial product.
- HIPAA: a BAA/add-on is not available on free tiers of any option checked (Supabase's HIPAA add-on is separate; plan requirement unverified). Do not store real PHI for US users on free tiers. HIPAA only applies if the operator is a covered entity or business associate, so a consumer app may fall outside it but could face FTC health-breach rules (UNVERIFIED).
- GDPR: health data is special-category; need explicit consent, a DPA with each processor, and EU region choice; free tiers rarely give DPA/region control (Supabase offers DPA/EU region generally; plan unclear).
- DPDP: obligations become fully enforceable 13 May 2027, so design consent, purpose limitation, deletion and breach notification now. The Act reportedly has no separate sensitive-data class (from the search summary only, UNVERIFIED).
- Data-loss risks on free tiers: Supabase no backups and weekly pausing; Render DB expiry; Atlas pause at 30 days; ephemeral Render/HF disk. Keep exports and use synthetic data in the prototype.

### Gaps
- Not verified: Supabase Free RLS/auth feature limits beyond MAU, Supabase pgvector on Free, Atlas Vector Search M0 limits, Neon pgvector (believed supported), HF Inference/ZeroGPU quotas, Cloudflare R2 free limits, Fly volume costs.
- Legal statements are brief orientation only, not legal advice; HIPAA/GDPR applicability to the specific app was not researched in primary sources.
