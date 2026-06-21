# Material de avaliação arquivado

Scripts, guias e figuras substituídos — mantidos para reprodutibilidade. **Não execute scripts daqui**; use [`../scripts/CATALOG.md`](../scripts/CATALOG.md).

## Propósito

Histórico de reorganizações (out–nov 2025, jun 2026) sem apagar evidência da monografia.

## Conteúdo

| Pasta / ficheiro | Conteúdo | Substituição canónica |
|------------------|----------|----------------------|
| `pruned_figures/2026-06/` | ~160 PNGs removidos (docx-only cleanup) | [`../02_graphs/MANIFEST.md`](../02_graphs/MANIFEST.md) |
| `old_graphs/` | PNGs API pré-reorg (out 2025) | [`../02_graphs/`](../02_graphs/README.md) |
| `2025-10_reorg_scripts/` | Antiga `04_scripts/` | [`../scripts/02_api_performance/`](../scripts/CATALOG.md) |
| `2025-11_duplicate_scripts/` | Cópias duplicadas | [`../scripts/`](../scripts/CATALOG.md) |
| `2025-11_superseded_guides/` | GUIA_* antigos | [`../scripts/CATALOG.md`](../scripts/CATALOG.md) |
| `2025-10_e2e_python/` | E2E Python legado | [`../scripts/03_api_e2e/`](../scripts/03_api_e2e/README.md) + Flutter E2E |
| `GUIA_INSERCAO_FIGURAS_FINAL.md` | Guia figuras nov 2025 | Não usado no docx actual |
| `MUDANCAS_FINAIS_RESUMO.txt` | Notas de simplificação | Histórico Git |

Deploy shell antigo (só build ECR): [`../../infra/archive/build-and-push-sentiment-image.sh`](../../infra/archive/build-and-push-sentiment-image.sh).

## Ver também

- [`../02_graphs/MANIFEST.md`](../02_graphs/MANIFEST.md)
- [`../README.md`](../README.md)
