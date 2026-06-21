# Frontend — YouTube Comment Reader

App mobile Flutter para pesquisar vídeos, ler comentários e filtrar por sentimento (via API em produção).

## Propósito

Interface do utilizador: busca de vídeos, comentários com rótulos POSITIVE/NEGATIVE/NEUTRAL, favoritos locais, ordenação e filtros. Suporta tema claro e escuro.

## Conteúdo

| Pasta | Finalidade |
|-------|------------|
| `lib/app/pages/` | Ecrãs: busca, comentários, favoritos |
| `lib/app/common/api/` | Cliente HTTP (`youtube_comment_viewer_api.dart`) |
| `lib/app/common/themes/` | Tema e tokens (`app_theme.dart`, `theme_tokens.dart`) |
| `integration_test/` | Testes E2E reais (Flutter) |
| `test/` | Testes unitários/widget |

## Como usar

```bash
cd packages/frontend
flutter pub get
flutter run
```

Credenciais Firebase: ficheiro `.env` nesta pasta (ver [`integration_test/README.md`](integration_test/README.md)).

## Testes E2E

Suite principal: `integration_test/tests/complete_all_features_test.dart` (14 testes). Tabela PNG para a monografia: gerada por [`../../evaluation/scripts/02_api_performance/generate_e2e_test_table.py`](../../evaluation/scripts/02_api_performance/generate_e2e_test_table.py) — ver [`../../evaluation/02_graphs/MANIFEST.md`](../../evaluation/02_graphs/MANIFEST.md).

## Ver também

- [`../README.md`](../README.md) — packages
- [`integration_test/README.md`](integration_test/README.md) — E2E detalhado
- [`../../evaluation/README.md`](../../evaluation/README.md) — avaliação
