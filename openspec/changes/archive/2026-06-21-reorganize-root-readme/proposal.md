## Why

The root `README.md` is only 17 lines and most folders lack orientation docs. After evaluation reorganizations (canonical scripts, unified `requirements.txt`, docx figure inventory), contributors cannot tell what each area contains or where to start. The agreed model is a **hierarchical README tree**: a short root index plus a **dedicated README in each major folder** explaining its contents—not a single deep `evaluation/README.md` alone.

Root `/scripts/` also collides mentally with `evaluation/scripts/`; deploy automation should live under a clearly named folder (`infra/`) with redundant scripts archived.

## What Changes

- **Root `README.md`**: project summary, quick start by audience, top-level map, links to every major folder README (not inline detail).
- **Per-folder READMEs** (create or expand): `packages/`, `packages/frontend/`, `packages/lambdas/`, `infra/`, `stacks/`, expanded `evaluation/README.md`, plus evaluation subfolders `01_reports/`, `02_graphs/`, `03_data/`, `05_guides/`; refresh existing domain READMEs where stale.
- **Deploy consolidation**: move `deploy-with-sentiment.sh` → `infra/`; archive duplicate `build-and-push-sentiment-image.sh`; remove empty `scripts/perf/`; retire root `/scripts/` folder; update `package.json` `deploy:dev`.
- **Cross-reference fixes**: no stale `02_graphs/english/` paths; catalog and layout specs updated for `infra/` deploy path.

## Capabilities

### New Capabilities

- `root-readme`: Structure and content rules for the repository root orientation page.
- `folder-readme`: Required README coverage, minimum sections, and linking rules for major repository folders.

### Modified Capabilities

- `evaluation-layout`: `02_graphs/` description; requirement that numbered evaluation subfolders document roles in local READMEs.
- `script-catalog`: Deployment script paths under `infra/` instead of root `scripts/`.

## Impact

- **Primary**: Root `README.md`, new/updated READMEs under `packages/`, `infra/`, `stacks/`, `evaluation/`
- **Secondary**: `package.json`, `evaluation/scripts/CATALOG.md`, removal of root `/scripts/`
- **Out of scope**: Rewriting long methodology guides (`05_guides/*.md` bodies), OpenSpec `openspec/` README, per-test folders (`api_load_testing/teste_*`), application source code changes
