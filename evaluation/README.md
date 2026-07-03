# Avaliação — YouTube Comment Reader

Ponto de entrada para relatórios, dados, scripts e material da monografia (três pilares: **modelo**, **API**, **app mobile**), incluindo a definição da infraestrutura do backend em AWS CDK.

## Propósito

Reproduzir e documentar a avaliação acadêmica: métricas do classificador, testes de carga Locust, testes E2E Flutter e figuras/tabelas embutidas no docx. Este README também centraliza os links para o código e os guias que antes constavam como apêndices da monografia.

## Material da monografia

| Conteúdo | Onde encontrar |
|----------|----------------|
| **Infraestrutura (AWS CDK)** | [`../stacks/YouTubeCommentReaderBackendStack.ts`](../stacks/YouTubeCommentReaderBackendStack.ts) — definição da stack (API Gateway, DynamoDB, Lambdas, warmup). Guia: [`../stacks/README.md`](../stacks/README.md). Deploy: [`../infra/README.md`](../infra/README.md) |
| **Pilar 1 — Modelo** | [`model_analysis/README.md`](model_analysis/README.md) · scripts em [`scripts/01_model_evaluation/`](scripts/CATALOG.md) · Figuras 23–24, Tabela 1 |
| **Pilar 2 — API** | [`api_load_testing/README.md`](api_load_testing/README.md) · scripts em [`scripts/02_api_performance/`](scripts/CATALOG.md) · Figuras 25–26, Tabela 3 |
| **Pilar 3 — App (E2E Flutter)** | [`../packages/frontend/integration_test/README.md`](../packages/frontend/integration_test/README.md) · Tabela 4 (`generate_e2e_test_table.py --thesis`) |
| **Figuras e tabelas do docx** | [`02_graphs/MANIFEST.md`](02_graphs/MANIFEST.md) — inventário e comandos de regeneração |
| **Índice de scripts** | [`scripts/CATALOG.md`](scripts/CATALOG.md) |

## Estrutura

### Pastas numeradas (artefatos curados)

| Pasta | README | Finalidade |
|-------|--------|------------|
| `01_reports/` | [`README.md`](01_reports/README.md) | Relatórios finais e de apoio |
| `02_graphs/` | [`README.md`](02_graphs/README.md) | Figuras/tabelas docx (MANIFEST) |
| `03_data/` | [`README.md`](03_data/README.md) | CSV/JSON canônicos |
| `05_guides/` | [`README.md`](05_guides/README.md) | Metodologia e texto da monografia |
| `06_archived/` | [`README.md`](06_archived/README.md) | Material histórico e figuras removidas |

`04_scripts/` — apenas redirect; scripts arquivados em `06_archived/`.

### Scripts vs saídas

| Pasta | Scripts? | Saídas |
|-------|----------|--------|
| [`scripts/`](scripts/README.md) | ✅ Canônico (`CATALOG.md`) | alguns `graphs/` locais |
| [`model_analysis/`](model_analysis/README.md) | redirect | `results/`, `graphs/`, `data/` |
| [`api_load_testing/`](api_load_testing/README.md) | redirect | `results/`, `teste_1..4/` |
| [`model_comparison/`](model_comparison/README.md) | scripts locais | `results/` (incl. Tabela 1 TXT) |

### Três pilares

| Pilar | Scripts | Saídas / figuras docx |
|-------|---------|------------------------|
| **1 — Modelo** | `scripts/01_model_evaluation/` | `model_analysis/` · Figura 23–24 · Tabela 1 |
| **2 — API** | `scripts/02_api_performance/` | `api_load_testing/` · Figura 25–26 · Tabela 3 |
| **3 — App** | `packages/frontend/integration_test/` | Tabela 4 PNG · [`02_graphs/tables/`](02_graphs/tables/) |

## Configuração

Python **3.10+**. Na raiz do repositório:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r evaluation/requirements.txt
python3 -m nltk.downloader vader_lexicon
```

## Como usar

```bash
# Modelo (exemplo)
cd evaluation/scripts/01_model_evaluation
python3 compare_metrics_vs_benchmark.py

# Performance da API
cd evaluation/scripts/02_api_performance
python3 run_all.py
```

Deploy do backend: [`../infra/README.md`](../infra/README.md) (não confundir com `evaluation/scripts/`). Código da stack: [`../stacks/YouTubeCommentReaderBackendStack.ts`](../stacks/YouTubeCommentReaderBackendStack.ts).

## Ver também

- [`scripts/CATALOG.md`](scripts/CATALOG.md) — índice de todos os scripts
- [`02_graphs/MANIFEST.md`](02_graphs/MANIFEST.md) — lista de figuras e tabelas do docx
- [`../stacks/README.md`](../stacks/README.md) — infraestrutura AWS CDK
- [`../infra/README.md`](../infra/README.md) — deploy (Docker ECR + CDK)
- [`../README.md`](../README.md) — visão geral do repositório
