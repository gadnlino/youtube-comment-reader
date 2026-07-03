# Figuras de avaliação removidas (2026-06)

Activos PNG retirados dos caminhos activos em `evaluation/` durante a limpeza da **lista de activos apenas do docx** (mudança OpenSpec `prune-unused-evaluation-images`).

## O que foi mantido

Apenas os sete activos do docx da monografia (Tabela 1–4, Figura 23–26) e os respectivos dados/geradores de suporte. As cópias canónicas estão em:

- [`evaluation/02_graphs/MANIFEST.md`](../../02_graphs/MANIFEST.md)
- [`evaluation/02_graphs/figures/`](../../02_graphs/figures/) — Figura 23–26
- [`evaluation/02_graphs/tables/`](../../02_graphs/tables/) — PNG da Tabela 4

## O que está aqui

- **~160 ficheiros PNG** movidos das pastas activas de avaliação (preservando caminhos relativos sob `evaluation/`)
- Pastas inteiras arquivadas: `02_graphs/english/`, `02_graphs/portuguese/`
- Todas as saídas de figuras em português (`*_pt*`, gráficos PT da API, gráficos de análise de idioma)
- Figuras de rascunho em markdown (`multiple_sets_*`, gráficos de relatórios Sentiment140/IMDB, execuções duplicadas com timestamp)

Inventário auxiliar: [`inventory-pruned.json`](inventory-pruned.json).

## Como restaurar um ficheiro

Copie deste arquivo de volta para o caminho original sob `evaluation/`, ou regenere com o script indicado em `02_graphs/MANIFEST.md`. Não foi feita eliminação definitiva.
