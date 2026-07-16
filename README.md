# YouTube Comment Reader

Aplicação mobile Flutter para ler comentários do YouTube com classificação de sentimento (TF-IDF + Regressão Logística), backend serverless na AWS e material de avaliação académica.

## O que é este repositório

- **App** — [`packages/frontend/`](packages/frontend/README.md): UI Flutter, tema claro/escuro, favoritos e filtros por sentimento.
- **API** — [`packages/lambdas/`](packages/lambdas/README.md) + [`stacks/`](stacks/README.md): API Gateway, Lambdas TypeScript e classificador Python em Docker.
- **Avaliação** — [`evaluation/`](evaluation/README.md): relatórios, scripts Python, figuras e tabelas da monografia.

Monorepo Node (CDK) + Flutter; scripts de **pesquisa** ficam em `evaluation/scripts/` (não confundir com `infra/`).

## Começar rápido

### App Flutter

```bash
cd packages/frontend
flutter pub get
```

Ver [`packages/frontend/README.md`](packages/frontend/README.md).

### Testes E2E (Pilar 3 — monografia)

```bash
cd packages/frontend
flutter drive --driver=test_driver/integration_test.dart \
  --target=integration_test/tests/complete_all_features_test.dart
```

Ver [`packages/frontend/integration_test/README.md`](packages/frontend/integration_test/README.md).

### Deploy do backend

```bash
npm install
npm run deploy:dev
```

Requisitos: Docker, AWS CLI, modelo em `packages/lambdas/sentiment_analysis/models/`. Ver [`infra/README.md`](infra/README.md).

### Avaliação Python

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r evaluation/requirements.txt
python3 -m nltk.downloader vader_lexicon
```

Ver [`evaluation/README.md`](evaluation/README.md).

## Mapa do repositório

| Pasta | README | Finalidade |
|-------|--------|------------|
| [`packages/`](packages/README.md) | ✓ | App Flutter + Lambdas AWS |
| [`infra/`](infra/README.md) | ✓ | Deploy (Docker ECR + CDK) |
| [`stacks/`](stacks/README.md) | ✓ | Definição CDK (`YouTubeCommentReaderBackendStack`) |
| [`evaluation/`](evaluation/README.md) | ✓ | Relatórios, dados, scripts e figuras da monografia |
| [`openspec/`](openspec/changes/) | — | Propostas de mudança OpenSpec |
| [`docs/`](docs/servicos-aws.md) | ✓ | Serviços da AWS/tecnologias, funções Lambda e diagrama ER |
| `cdk.ts` | — | Entrada CDK na raiz |

## Documentação

| Tópico | Onde |
|--------|------|
| Serviços da AWS e tecnologias utilizados | [`docs/servicos-aws.md`](docs/servicos-aws.md) |
| Funções Lambda da camada intermediária | [`docs/funcoes-lambda.md`](docs/funcoes-lambda.md) |
| Índice da avaliação | [`evaluation/README.md`](evaluation/README.md) |
| Scripts executáveis | [`evaluation/scripts/CATALOG.md`](evaluation/scripts/CATALOG.md) |
| Figuras/tabelas docx | [`evaluation/02_graphs/MANIFEST.md`](evaluation/02_graphs/MANIFEST.md) |
| Relatório final | [`evaluation/01_reports/FINAL_EVALUATION_REPORT.md`](evaluation/01_reports/FINAL_EVALUATION_REPORT.md) |
| Texto monografia | [`evaluation/05_guides/TEXTO_AVALIACAO_MONOGRAFIA.md`](evaluation/05_guides/TEXTO_AVALIACAO_MONOGRAFIA.md) |

Licença: Apache-2.0 (ver [`package.json`](package.json)).
