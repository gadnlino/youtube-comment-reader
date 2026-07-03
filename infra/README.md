# Infraestrutura — Deploy

Scripts de implantação do backend (Docker + ECR + AWS CDK). Substitui a antiga pasta raiz `/scripts/`.

## Propósito

Publicar a imagem Docker do classificador de sentimento e implantar a stack `YouTubeCommentReaderBackendStack` com o digest ECR correto.

## Conteúdo

| Arquivo | Finalidade |
|----------|------------|
| `deploy-with-sentiment.sh` | Fluxo completo: pré-requisitos → build → push ECR → `cdk deploy` |
| `archive/build-and-push-sentiment-image.sh` | **Arquivado** — apenas build/push (subconjunto do script acima) |

## Como usar

Na raiz do repositório:

```bash
npm install
npm run deploy:dev
```

Equivalente a `bash infra/deploy-with-sentiment.sh`.

**Pré-requisitos:** Docker em execução, AWS CLI configurado, arquivo `packages/lambdas/sentiment_analysis/models/tfidf_logistic_model.pkl`.

Variáveis opcionais: `AWS_REGION`, `AWS_ACCOUNT_ID`, `IMAGE_TAG`.

## Ver também

- [`../stacks/README.md`](../stacks/README.md) — o que o CDK cria
- [`../packages/lambdas/README.md`](../packages/lambdas/README.md) — funções implantadas
- [`../evaluation/scripts/CATALOG.md`](../evaluation/scripts/CATALOG.md) — entrada «implantacao»
