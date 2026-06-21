## 1. Deploy consolidation

- [x] 1.1 Create `infra/` and move `scripts/deploy-with-sentiment.sh` → `infra/deploy-with-sentiment.sh`
- [x] 1.2 Update `package.json` `deploy:dev` to `bash infra/deploy-with-sentiment.sh`
- [x] 1.3 Archive `scripts/build-and-push-sentiment-image.sh` to `infra/archive/` with note in `infra/README.md`
- [x] 1.4 Remove empty `scripts/perf/` and retire root `scripts/` folder
- [x] 1.5 Update `evaluation/scripts/CATALOG.md` deployment rows for `infra/deploy-with-sentiment.sh`

## 2. Root README

- [x] 2.1 Rewrite `README.md`: title, description, quick start (app, E2E, deploy, evaluation)
- [x] 2.2 Add repository map linking each major folder to its README (`packages/`, `infra/`, `stacks/`, `evaluation/`, `openspec/`)
- [x] 2.3 Add documentation index (folder READMEs + MANIFEST + CATALOG); keep under 120 lines

## 3. Application & infrastructure READMEs

- [x] 3.1 Create `packages/README.md` (monorepo overview, links to frontend/lambdas)
- [x] 3.2 Replace `packages/frontend/README.md` (app purpose, structure, setup, link to integration_test)
- [x] 3.3 Create `packages/lambdas/README.md` (ycv_api, sentiment_analysis, warmup)
- [x] 3.4 Create `infra/README.md` (deploy prerequisites, `npm run deploy:dev`, archived build script)
- [x] 3.5 Create `stacks/README.md` (CDK stack role, link to `cdk.ts`)

## 4. Evaluation README tree

- [x] 4.1 Expand `evaluation/README.md` (full map, three pillars, links to all child READMEs)
- [x] 4.2 Create `evaluation/01_reports/README.md`
- [x] 4.3 Create `evaluation/02_graphs/README.md` (→ MANIFEST, figures/, tables/)
- [x] 4.4 Create `evaluation/03_data/README.md`
- [x] 4.5 Create `evaluation/05_guides/README.md`
- [x] 4.6 Update `evaluation/06_archived/README.md` if paths stale (pruned_figures, etc.)
- [x] 4.7 Refresh `evaluation/model_analysis/README.md`, verify `api_load_testing/` and `model_comparison/` READMEs
- [x] 4.8 Verify `evaluation/scripts/README.md` links and stale path cleanup

## 5. Cleanup & verification

- [x] 5.1 Handle orphan root `graphs/` if present (archive duplicate E2E PNG)
- [x] 5.2 Grep repo for `scripts/deploy-with-sentiment`, `scripts/build-and-push`, `02_graphs/english`, broken README links
- [x] 5.3 Confirm all new READMEs follow minimum structure (purpose, contents, how to use, see also)
