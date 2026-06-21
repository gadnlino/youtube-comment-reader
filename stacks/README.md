# Stacks — AWS CDK

Definição da infraestrutura cloud do backend.

## Propósito

Stack CDK que provisiona API Gateway, DynamoDB (cache), Lambdas TypeScript (`ycv_api`), Lambda Python de sentimento (imagem ECR) e warmup.

## Conteúdo

| Ficheiro | Finalidade |
|----------|------------|
| `YouTubeCommentReaderBackendStack.ts` | Stack principal (recursos e outputs) |
| `../cdk.ts` | Entrada CDK (`ENV_NAME`, conta/região) |

A Lambda de sentimento usa `IMAGE_DIGEST` (env no deploy ou valor em código) para fixar a imagem ECR.

## Como usar

Normalmente via [`../infra/deploy-with-sentiment.sh`](../infra/deploy-with-sentiment.sh):

```bash
npm run deploy:dev
```

Sintetizar sem deploy: `npx cdk synth` (na raiz).

## Ver também

- [`../infra/README.md`](../infra/README.md) — deploy
- [`../packages/lambdas/README.md`](../packages/lambdas/README.md) — código das funções
