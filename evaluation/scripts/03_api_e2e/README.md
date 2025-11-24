# Scripts de Testes End-to-End da API

Esta pasta contém os scripts de testes end-to-end que validam o fluxo completo da **API backend**, desde a busca de vídeos até a filtragem de comentários por sentimento.

> **Nota**: Estes são testes da **API backend** (Python). Para testes E2E completos incluindo a interface do usuário, consulte os testes Flutter em `packages/frontend/integration_test/`.

## 📋 Visão Geral

Os testes E2E da API validam:
- **Fluxo completo do backend**: Busca → Carregamento → Filtragem
- **Integração entre componentes**: API Gateway → Lambda → YouTube API → Sentiment Analysis
- **Acurácia da filtragem**: Verificação de que os filtros retornam apenas comentários com o sentimento correto
- **Tratamento de erros**: Comportamento em cenários de erro

## 📁 Scripts

### Teste Principal

- **`e2e_functionality_test.py`**: Script principal de testes E2E da API

  Testa os seguintes cenários:
  1. ✅ Busca de vídeos
  2. ✅ Carregamento de comentários sem análise de sentimento
  3. ✅ Carregamento de comentários com análise de sentimento
  4. ✅ Filtragem por comentários positivos
  5. ✅ Filtragem por comentários negativos
  6. ✅ Filtragem por comentários neutros
  7. ⚠️ Tratamento de erros (vídeos inválidos)

## 🚀 Como Usar

### Pré-requisitos

```bash
pip install requests
```

### Executar os Testes

```bash
cd evaluation/scripts/03_api_e2e
python e2e_functionality_test.py
```

### Configuração

Edite o script para configurar:
```python
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"
TEST_VIDEO_ID = "dQw4w9WgXcQ"  # ID do vídeo para teste
```

## 📊 Resultados

O script gera:
- **Arquivo JSON**: Relatório completo dos testes (salvo como `e2e_test_report_TIMESTAMP.json`)
- **Saída no console**: Resultados em tempo real

### Exemplo de Saída

```
✅ PASS: Search Videos
✅ PASS: Fetch Comments (No Sentiment)
✅ PASS: Fetch Comments (With Sentiment)
✅ PASS: Filter Positive Comments (100% accuracy)
✅ PASS: Filter Negative Comments (100% accuracy)
✅ PASS: Filter Neutral Comments (100% accuracy)
⚠️ FAIL: Error Handling

Tests Passed: 5/6 (83.3%)
Filter Accuracy: 100% (100/100 comments)
```

## 📈 Métricas Validadas

### Acurácia de Filtragem

O teste valida que **100% dos comentários retornados** têm o sentimento correto:
- **Filtro Positivo**: Todos os comentários retornados são positivos
- **Filtro Negativo**: Todos os comentários retornados são negativos
- **Filtro Neutro**: Todos os comentários retornados são neutros

### Distribuição de Sentimentos

O teste também valida a distribuição de sentimentos:
- Percentual de comentários positivos
- Percentual de comentários negativos
- Percentual de comentários neutros

## 🔗 Referências

- **Relatório completo de resultados**: `../../e2e_functionality_testing/E2E_FUNCTIONALITY_UX_RESULTS.md`
- **Dados brutos**: `../../e2e_functionality_testing/e2e_test_report_*.json`
- **Relatórios de avaliação**: `../../01_reports/`
- **Testes E2E do frontend**: `../../../../packages/frontend/integration_test/` (testes Flutter com renderização real da UI)

## 📝 Notas Importantes

- ⚠️ **Estes testes validam apenas a API backend** (endpoints HTTP)
- ✅ **Para testes E2E completos incluindo a interface do usuário**, consulte os testes Flutter em `packages/frontend/integration_test/`
- Os testes são executados contra a API em produção (AWS API Gateway + Lambda)
- Os testes do frontend (Flutter) testam a interface completa, incluindo renderização, interações do usuário e navegação

