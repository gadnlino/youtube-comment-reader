# Packages

Monorepo das aplicações do YouTube Comment Reader (`pnpm-workspace.yaml` inclui `packages/**/*`).

## Propósito

Código executável do produto: cliente mobile e funções AWS. A avaliação académica vive em [`../evaluation/`](../evaluation/README.md), não aqui.

## Conteúdo

| Pasta | Finalidade | README |
|-------|------------|--------|
| `frontend/` | App Flutter (Android/iOS) | [`frontend/README.md`](frontend/README.md) |
| `lambdas/` | Backend serverless | [`lambdas/README.md`](lambdas/README.md) |

## Como usar

```bash
# Flutter
cd frontend && flutter pub get

# Lambdas (via CDK na raiz)
cd ../.. && npm install && npm run deploy:dev
```

## Ver também

- [`../README.md`](../README.md) — visão geral do repositório
- [`../infra/README.md`](../infra/README.md) — deploy
- [`../stacks/README.md`](../stacks/README.md) — stack CDK
