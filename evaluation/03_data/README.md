# Dados — `03_data/`

CSV e JSON canónicos usados como entrada ou resumo nas avaliações.

## Propósito

Separar **dados versionados** de saídas geradas (`model_analysis/results/`, `api_load_testing/results/`).

## Conteúdo

| Subpasta | Finalidade |
|----------|------------|
| `csv/` | Datasets tabulares (ex.: comentários, exports) |
| `json/` | Listas de vídeos, resumos estruturados |

Muitos scripts também leem/escrevem em pastas de domínio; ver [`../scripts/CATALOG.md`](../scripts/CATALOG.md).

## Como usar

Consultar ficheiros directamente ou apontar scripts para estes paths (ver docstring de cada script em `../scripts/`).

## Ver também

- [`../model_analysis/data/`](../model_analysis/README.md) — JSON de trabalho do modelo
- [`../scripts/_paths.py`](../scripts/_paths.py) — constantes de caminho partilhadas
