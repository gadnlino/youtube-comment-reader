# Pruned evaluation figures (2026-06)

PNG assets removed from active `evaluation/` paths during the **docx-only keep-list** cleanup (`prune-unused-evaluation-images` OpenSpec change).

## What was kept

Only the seven thesis docx assets (Tabela 1–4, Figura 23–26) and their backing data/generators. Canonical copies live under:

- [`evaluation/02_graphs/MANIFEST.md`](../../02_graphs/MANIFEST.md)
- [`evaluation/02_graphs/figures/`](../../02_graphs/figures/) — Figura 23–26
- [`evaluation/02_graphs/tables/`](../../02_graphs/tables/) — Tabela 4 PNG

## What is here

- **~160 PNG files** moved from active evaluation folders (preserving relative paths under `evaluation/`)
- Entire archived folders: `02_graphs/english/`, `02_graphs/portuguese/`
- All Portuguese-labelled figure outputs (`*_pt*`, API PT charts, language-analysis charts)
- Markdown-draft figures (`multiple_sets_*`, Sentiment140/IMDB report charts, duplicate timestamp runs)

Sidecar inventory: [`inventory-pruned.json`](inventory-pruned.json).

## Restoring a file

Copy from this archive back to the original path under `evaluation/`, or regenerate via the script listed in `02_graphs/MANIFEST.md`. Hard deletion was not performed.
