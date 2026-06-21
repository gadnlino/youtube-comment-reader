# Lambdas — Backend AWS

Funções serverless que expõem a API do YouTube Comment Reader e classificam sentimento.

## Propósito

Backend em produção: listar/buscar vídeos e comentários (YouTube API) e classificar texto com TF-IDF + Regressão Logística num container Python.

## Conteúdo

| Pasta | Runtime | Finalidade |
|-------|---------|------------|
| `ycv_api/` | TypeScript (Node.js) | Endpoints REST: vídeos, comentários, busca |
| `sentiment_analysis/` | Python (Docker → ECR) | Lambda de classificação de sentimento |
| `warmup/` | TypeScript | Warmup periódico (cold start) |

Modelo treinado: `sentiment_analysis/models/tfidf_logistic_model.pkl` (obrigatório antes do deploy).

## Como usar

Deploy completo a partir da raiz:

```bash
npm install
npm run deploy:dev
```

Isto executa [`../../infra/deploy-with-sentiment.sh`](../../infra/deploy-with-sentiment.sh) (build Docker, push ECR, `cdk deploy`).

## Ver também

- [`../../infra/README.md`](../../infra/README.md) — pré-requisitos de deploy
- [`../../stacks/README.md`](../../stacks/README.md) — recursos CDK
- [`../../evaluation/README.md`](../../evaluation/README.md) — avaliação do modelo e da API
