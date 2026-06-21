## Context

The **docx** (not the markdown draft) defines the thesis asset set. Author uploaded **7 screenshots**:

| Docx ref | Type | Repo match | Generator / source |
|----------|------|------------|-------------------|
| **Tabela 1** | Word table | `model_comparison/results/comprehensive_model_comparison.txt` | `comprehensive_model_comparison.py` |
| **Tabela 3** | Word table | Locust/consolidated data; `consolidated_table_only.png` (reference) | `generate_consolidated_graphs.py` |
| **Tabela 4** | Word table | **Missing PNG** `e2e_test_results_table_20251102.png` | `generate_e2e_test_table.py` |
| **Figura 23** | Chart | `metrics_per_class_tfidf_lr_amitzala_youtube-comments-with-labeled_20260317_230701.png` | `evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py` + CSV |
| **Figura 24** | Chart | `scripts/graphs/tfidf_lr_selection_vs_kaggle_amitzala_20260621_172335.png` | `plot_tfidf_lr_selection_vs_kaggle_amitzala.py` |
| **Figura 25** | Dashboard | `consolidated_graphs_part1.png` | `generate_consolidated_graphs.py` |
| **Figura 26** | Dashboard | `consolidated_graphs_part2.png` | `generate_consolidated_graphs.py` |

### Explicitly **not** on keep-list (author decision)

| Category | Examples | Action |
|----------|----------|--------|
| Markdown-draft figures | `multiple_sets_overall_bias_ci95_*.png`, `multiple_sets_bias_by_set_*.png` | Archive |
| Markdown Tabela 2 | Inline table in `TEXTO_AVALIACAO_MONOGRAFIA.md` | Text stays in repo; **not** a protected figure asset |
| All PT figure outputs | `*_pt.png`, `*pt_*.png`, `boxplot_viés_linguistico_pt_*`, `comparacao_tempo_medio_resposta_pt.png`, etc. | Archive (~30+ PNGs) |
| `02_graphs/english/` + `portuguese/` | 10 curated EN/PT performance figures | **Archive entire folders** |
| Sentiment140 / IMDB validation charts | Report PNGs not in docx | Archive |

**Note:** PT **scripts** (`validate_with_tweets_pt.py`, `generate_language_analysis_graphs_pt.py`, etc.) are **not** archived—they remain runnable code; only their **output PNGs** and unused PT graph folders are archived.

```
┌─────────────────────────────────────────────────────────────┐
│  DOCX-ONLY KEEP-LIST                                         │
├─────────────────────────────────────────────────────────────┤
│  7 docx assets (Tab 1–4, Fig 23–26)                          │
│       ↓                                                      │
│  Canonical PNG / TXT / CSV + generators                      │
│       ↓                                                      │
│  evaluation/02_graphs/MANIFEST.md (flat layout)              │
├─────────────────────────────────────────────────────────────┤
│  ARCHIVE: everything else (*.png not in closure)              │
│           + 02_graphs/english/ + portuguese/                 │
│           + all *_pt* figure PNGs                            │
└─────────────────────────────────────────────────────────────┘
```

## Goals / Non-Goals

**Goals:**

- Docx-only keep-list with backing-data closure.
- Archive PT figure assets and EN/PT curated folders.
- One canonical copy per docx figure under `02_graphs/figures/` or `02_graphs/tables/`.
- Scripts that regenerate kept assets still run after cleanup.

**Non-Goals:**

- Archiving PT Python validation scripts (code stays).
- Keeping markdown-draft figure set.
- Hard delete.

## Decisions

### 1. Keep-list source: docx only

**Decision:** Keep-list = 7 uploaded docx assets + their backing files and generators. `TEXTO_AVALIACAO_MONOGRAFIA.md` is **not** a keep-list source for figures.

### 2. PT assets: archive figures, keep scripts

**Decision:** Grep/archive all evaluation PNGs matching PT figure patterns. Do **not** remove `*_pt.py` scripts unless they have no non-archived purpose (out of scope).

### 3. Replace `02_graphs/english/` and `portuguese/`

**Decision:** Archive both subfolders entirely. New structure:

```
evaluation/02_graphs/
├── MANIFEST.md
├── inventory.json
├── figures/     ← Fig 23, 24, 25, 26 canonical copies
└── tables/      ← Tabela 4 PNG when regenerated
```

Tabela 1 and 3 remain sourced from TXT/data paths documented in manifest (not necessarily copied as PNG).

### 4. Duplicate timestamps

Keep newest per logical docx figure (e.g. one `tfidf_lr_selection_vs_kaggle_amitzala_*`); archive older runs and all non-docx PNGs.

### 5. Script verification (unchanged)

Smoke-test: `plot_tfidf_lr_selection_vs_kaggle_amitzala.py`, `evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py`, `comprehensive_model_comparison.py`, `generate_consolidated_graphs.py`, `generate_e2e_test_table.py`.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| `TEXTO_AVALIACAO_MONOGRAFIA.md` still cites archived figures | Update markdown to point to docx set or note archived; optional follow-up |
| Accidentally archive backing CSV for docx tables | Inventory marks keep-backing before any move |
| PT scripts regenerate PT PNGs on run | Document in manifest; new outputs go to domain folders, not keep-list |

## Open Questions

None blocking—author confirmed docx-only, drop PT figures, drop `02_graphs` language folders.
