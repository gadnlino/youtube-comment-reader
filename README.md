# youtube-comment-reader

## Estrutura do repositório

| Caminho | Finalidade |
|---------|------------|
| `packages/frontend/` | Aplicação mobile Flutter |
| `packages/lambdas/` | Backend AWS Lambda |
| `scripts/` | **Implantação** — scripts shell de build Docker e deploy |
| `evaluation/` | **Pesquisa e testes** — relatórios, dados, scripts Python de avaliação |
| `evaluation/scripts/` | Scripts canónicos de avaliação — ver `evaluation/scripts/CATALOG.md` |
| `openspec/` | Propostas de mudança OpenSpec |

**Implantar:** `scripts/build-and-push-sentiment-image.sh`, `scripts/deploy-with-sentiment.sh`

**Avaliar:** `evaluation/README.md`
