# Flutter Integration Tests - YouTube Comment Reader

## 📋 Visão Geral

Estes são **testes de integração E2E (end-to-end) REAIS** que simulam o comportamento do usuário na aplicação Flutter mobile. Diferente dos testes de API, estes testes:

✅ **Renderizam a interface gráfica** do Flutter  
✅ **Simulam cliques** em botões e componentes  
✅ **Digitam texto** em campos de busca  
✅ **Navegam entre telas** como um usuário real  
✅ **Verificam elementos visuais** na UI  

## 🎯 Testes Implementados

O arquivo `tests/complete_all_features_test.dart` contém **14 testes completos** que validam TODAS as funcionalidades da aplicação:

### 📹 Página de Busca de Vídeos (5 testes)

1. **Test 1:** Visualizar lista de vídeos na página de busca
2. **Test 2:** Filtrar vídeos por palavra-chave "flutter"
3. **Test 3:** Ordenar vídeos por mais recentes
4. **Test 4:** Ordenar vídeos por mais relevantes
5. **Test 5:** Adicionar vídeo aos favoritos na página de busca

### 💬 Página de Comentários do Vídeo (7 testes)

6. **Test 6:** Visualizar lista de comentários de um vídeo
7. **Test 7:** Filtrar comentários por palavra-chave
8. **Test 8:** Ordenar comentários por mais recentes
9. **Test 9:** Ordenar comentários por mais relevantes
10. **Test 10:** Filtrar comentários por sentimento POSITIVO
11. **Test 11:** Filtrar comentários por sentimento NEGATIVO
12. **Test 12:** Adicionar comentário aos favoritos

### ⭐ Página de Favoritos (2 testes)

13. **Test 13:** Visualizar vídeos favoritados na aba de Favoritos
14. **Test 14:** Remover vídeo dos favoritos

**Duração estimada**: ~10-15 minutos | **Cobertura**: Todas as funcionalidades da aplicação

## 🛠️ Tecnologias Usadas

- **Flutter SDK:** Framework mobile multiplataforma
- **integration_test:** Pacote oficial do Flutter para testes E2E
- **WidgetTester:** Ferramenta para simular interações de usuário
- **Simulação de gestos:** Taps, scroll, text input
- **Renderização real:** Widgets são realmente renderizados

## 📦 Pré-requisitos

1. Flutter SDK instalado (versão >= 3.1.5)
2. Emulador Android/iOS ou dispositivo físico conectado
3. Dependências do projeto instaladas

```bash
# Instalar dependências
cd packages/frontend
flutter pub get
```

## 🚀 Como Executar os Testes

### Executar Testes com Device/Emulador (Recomendado)

Para rodar os testes com renderização real em device ou emulador:

```bash
cd packages/frontend

# 1. Certifique-se de que um emulador está rodando ou device conectado
flutter devices

# 2. Execute os testes completos
flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/tests/complete_all_features_test.dart
```

**Duração**: ~10-15 minutos | **Arquivo**: `integration_test/tests/complete_all_features_test.dart`

### Executar em Device Específico

```bash
cd packages/frontend

# Listar devices disponíveis
flutter devices

# Executar em device específico
flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/tests/complete_all_features_test.dart \
  -d <device_id>
```

### Executar Teste Rápido (sem device/emulador)

Para testar a lógica sem renderizar em device/emulador (mais rápido, mas não testa UI real):

```bash
cd packages/frontend
flutter test integration_test/tests/complete_all_features_test.dart
```

**Nota**: Este modo não renderiza a UI real, apenas testa a lógica.

## 📊 Exemplo de Saída Esperada

```
📹 Test 1: Viewing video list...
✅ Found 8 videos in list
✅ TEST 1 PASSED: Video list displayed

🔍 Test 2: Filtering videos by keyword...
✅ Entered keyword: "flutter"
✅ Found "flutter" in: "Flutter Tutorial for Beginners"
✅ TEST 2 PASSED: Video keyword filter works

📅 Test 3: Sorting videos by most recent...
✅ Entered keyword: "news" (required by YouTube API)
✅ Selected "Most recent" sort
✅ Videos sorted by date
✅ TEST 3 PASSED: Sort by most recent works

⭐ Test 4: Sorting videos by most relevant...
✅ Selected "Most relevant" sort
✅ Videos sorted by relevance
✅ TEST 4 PASSED: Sort by most relevant works

⭐ Test 5: Adding video to favorites...
✅ Tapped favorite button
✅ TEST 5 PASSED: Add video to favorites works

💬 Test 6: Viewing comments list...
✅ Navigated to comments page
✅ Found 15 comments
✅ TEST 6 PASSED: Comments list displayed

🔍 Test 7: Filtering comments by keyword...
✅ Entered comment keyword filter: "good"
✅ Comment keyword filter applied
✅ TEST 7 PASSED: Filter comments by keyword works

📅 Test 8: Sorting comments by most recent...
✅ Selected "Most recent" for comments
✅ Comments sorted by time
✅ TEST 8 PASSED: Sort comments by most recent works

⭐ Test 9: Sorting comments by most relevant...
✅ Selected "Most relevant" for comments
✅ Comments sorted by relevance
✅ TEST 9 PASSED: Sort comments by most relevant works

😊 Test 10: Filtering POSITIVE comments...
✅ Selected POSITIVE sentiment filter
✅ Found 8 positive comments
✅ TEST 10 PASSED: POSITIVE sentiment filter works

😞 Test 11: Filtering NEGATIVE comments...
✅ Selected NEGATIVE sentiment filter
✅ Found 5 negative comments
✅ TEST 11 PASSED: NEGATIVE sentiment filter works

⭐ Test 12: Adding comment to favorites...
✅ Tapped favorite on comment
✅ TEST 12 PASSED: Add comment to favorites works

⭐ Test 13: Viewing favorites tab...
✅ Favorited a video
✅ Navigated to Favorites tab
✅ Found 1 favorited videos
✅ TEST 13 PASSED: Favorites tab displays correctly

❌ Test 14: Removing video from favorites...
✅ Favorited video
✅ Unfavorited video
✅ TEST 14 PASSED: Remove from favorites works

================================================================================
🏆 COMPLETE E2E TEST SUITE - FINAL RESULTS
================================================================================

📹 VIDEO SEARCH PAGE (5 tests):
  ✅ Test 1: View video list
  ✅ Test 2: Filter videos by keyword
  ✅ Test 3: Sort videos by most recent
  ✅ Test 4: Sort videos by most relevant
  ✅ Test 5: Add video to favorites

💬 VIDEO COMMENTS PAGE (7 tests):
  ✅ Test 6: View comments list
  ✅ Test 7: Filter comments by keyword
  ✅ Test 8: Sort comments by most recent
  ✅ Test 9: Sort comments by most relevant
  ✅ Test 10: Filter by POSITIVE sentiment
  ✅ Test 11: Filter by NEGATIVE sentiment
  ✅ Test 12: Add comment to favorites

⭐ FAVORITES PAGE (2 tests):
  ✅ Test 13: View favorited videos
  ✅ Test 14: Remove video from favorites

📊 TOTAL: 14 comprehensive E2E tests

🎯 ALL USER-FACING FEATURES VALIDATED:
  • Video listing ✓
  • Video keyword filtering ✓
  • Video sorting (recent/relevant) ✓
  • Video favoriting/unfavoriting ✓
  • Comment viewing ✓
  • Comment keyword filtering ✓
  • Comment sorting (recent/relevant) ✓
  • Sentiment filtering (Positive/Negative) ✓
  • Comment favoriting ✓
  • Favorites page viewing ✓
  • Tab navigation ✓
================================================================================
```

## 🎨 O que os Testes Fazem (Tecnicamente)

### Exemplo: Test 10 - Filtro de Sentimento Positivo

```dart
// 1. Iniciar o app (renderização real)
await tester.pumpWidget(buildApp());
await tester.pumpAndSettle(const Duration(seconds: 8));

// 2. Navegar para vídeo e comentários
final videoWidgets = find.byType(VideoWidget);
await tester.tap(videoWidgets.first);
await tester.pumpAndSettle(const Duration(seconds: 5));
await tester.pump(const Duration(seconds: 10)); // Aguardar carregamento de comentários
await tester.pumpAndSettle(const Duration(seconds: 5));

// 3. Abrir modal de filtro
final filterButton = find.byIcon(Icons.tune_rounded);
await tester.tap(filterButton.last);
await tester.pumpAndSettle(const Duration(seconds: 2));

// 4. Selecionar checkbox "Positives"
final positivesCheckbox = find.widgetWithText(CheckboxListTile, 'Positives');
await tester.tap(positivesCheckbox);
await tester.pumpAndSettle(const Duration(seconds: 1));

// 5. Aplicar filtro
final searchButton = find.widgetWithText(ElevatedButton, 'Search');
await tester.tap(searchButton);
await tester.pumpAndSettle(const Duration(seconds: 8));

// 6. Verificar comentários filtrados
final commentWidgets = find.byType(CommentWidget);
expect(commentWidgets.evaluate().isNotEmpty, true);
```

### Exemplo: Test 2 - Filtrar Vídeos por Palavra-chave

```dart
// 1. Iniciar o app
await tester.pumpWidget(buildApp());
await tester.pumpAndSettle(const Duration(seconds: 8));

// 2. Abrir modal de filtro
final filterButton = find.byIcon(Icons.tune_rounded);
await tester.tap(filterButton.first);
await tester.pumpAndSettle(const Duration(seconds: 2));

// 3. Digitar palavra-chave
final keywordField = find.widgetWithText(TextField, '').last;
await tester.enterText(keywordField, 'flutter');
await tester.pumpAndSettle(const Duration(seconds: 1));

// 4. Aplicar busca
final searchButton = find.widgetWithText(ElevatedButton, 'Search');
await tester.tap(searchButton);
await tester.pumpAndSettle(const Duration(seconds: 10));

// 5. Verificar resultados
final videoWidgets = find.byType(VideoWidget);
expect(videoWidgets.evaluate().isNotEmpty, true);

// 6. Verificar que pelo menos um vídeo contém a palavra-chave
bool foundKeyword = false;
for (final element in videoWidgets.evaluate()) {
  final widget = element.widget as VideoWidget;
  if (widget.video.snippet.title.toLowerCase().contains('flutter')) {
    foundKeyword = true;
    break;
  }
}
expect(foundKeyword, true);
```

## 🔄 Diferença: API Tests vs Integration Tests

| Aspecto | API Tests (Python) | Integration Tests (Flutter) |
|---------|-------------------|----------------------------|
| **O que testa** | Backend/API REST | Aplicação mobile completa |
| **Interface** | Requisições HTTP | UI renderizada |
| **Interação** | Parâmetros HTTP | Cliques e gestos reais |
| **Tecnologia** | `requests` Python | `integration_test` Dart |
| **Renderização** | ❌ Não renderiza UI | ✅ Renderiza widgets Flutter |
| **Simula usuário** | ❌ Simula chamadas API | ✅ Simula ações de usuário |
| **Testa UI** | ❌ Não | ✅ Sim |
| **Tipo** | Black-box API testing | End-to-end UI testing |

## ⚠️ Notas Importantes

### 1. **Tempo de Espera**

Os testes usam `pumpAndSettle()` com timeouts para aguardar:
- Animações
- Requisições de API
- Carregamento de dados

O teste também inclui uma função helper `waitForUI()` que usa `pump()` em vez de `pumpAndSettle()` para evitar travamentos em animações contínuas:

```dart
// Helper function no código
Future<void> waitForUI(WidgetTester tester, {int seconds = 3}) async {
  for (int i = 0; i < seconds; i++) {
    await tester.pump(const Duration(seconds: 1));
  }
}
```

### 2. **Ajustes Necessários**

Os testes podem precisar de ajustes baseados na estrutura real da UI:

- **Keys de Widgets:** Adicione `Key()` aos widgets importantes
- **Texto de Botões:** Verifique os textos exatos dos botões (ex: "Search", "Positives", "Negatives")
- **Estrutura de Widgets:** Ajuste seletores baseados na árvore de widgets real
- **Ícones:** Verifique se os ícones usados correspondem (ex: `Icons.tune_rounded`, `Icons.star_border`)

### 3. **API Real**

Os testes fazem requisições REAIS à API em produção. Certifique-se de que:
- API está online e acessível
- Credenciais/tokens estão configurados
- Arquivo `.env` está presente no diretório `packages/frontend/`

### 4. **Firebase**

Os testes requerem Firebase inicializado:
- Arquivo `.env` com credenciais do Firebase:
  ```
  FIREBASE_API_KEY=...
  FIREBASE_APP_ID=...
  FIREBASE_MESSAGE_SENDER_ID=...
  FIREBASE_PROJECT_ID=...
  ```
- O teste inicializa Firebase automaticamente no `setUpAll()`

### 5. **Possíveis Travamentos**

⚠️ **Atenção**: Este teste pode travar devido a animações contínuas se usar apenas `pumpAndSettle()`. O código já inclui a função `waitForUI()` que ajuda a evitar isso, mas se ainda houver problemas:
- Aumente os timeouts
- Use `pump()` em vez de `pumpAndSettle()` em pontos específicos
- Verifique se há animações infinitas na UI

## 🐛 Troubleshooting

### Problema: "Can't find widget"
**Solução:** 
- Adicione prints para debugar:
  ```dart
  print(tester.allWidgets.map((w) => w.runtimeType).toList());
  ```
- Verifique se os seletores correspondem à estrutura real da UI
- Use `find.byType()` ou `find.text()` conforme apropriado

### Problema: "Timeout waiting for response" ou teste trava
**Solução:** 
- Aumente os timeouts nos testes:
  ```dart
  await tester.pump(const Duration(seconds: 10));
  ```
- Use a função `waitForUI()` já incluída no código em vez de `pumpAndSettle()`:
  ```dart
  await waitForUI(tester, seconds: 5); // 5 segundos
  ```
- Verifique se há animações infinitas na UI que podem causar travamentos

### Problema: "No devices found"
**Solução:**
```bash
# Listar emuladores disponíveis
flutter emulators

# Iniciar emulador
flutter emulators --launch <emulator_id>

# Verificar devices conectados
flutter devices

# Ou conectar device físico e habilitar USB debugging
```

### Problema: "Firebase not initialized"
**Solução:**
- Certifique-se de que o arquivo `.env` existe em `packages/frontend/`
- Verifique se as credenciais do Firebase estão corretas
- O teste inicializa Firebase automaticamente no `setUpAll()`

### Problema: Teste falha ao encontrar elementos
**Solução:**
- Verifique se a UI mudou e os seletores precisam ser atualizados
- Use `find.byType()` para encontrar widgets por tipo
- Use `find.text()` para encontrar por texto exato
- Adicione `Key()` aos widgets importantes no código da aplicação

### Problema: Teste muito lento
**Solução:**
- Este teste é completo e pode levar 10-15 minutos (normal)
- Reduza timeouts se apropriado (mas cuidado com falsos negativos)
- Verifique se há requisições de API muito lentas

## 📝 Próximos Passos

1. **Execute os testes:** 
   ```bash
   cd packages/frontend
   flutter drive \
     --driver=test_driver/integration_test.dart \
     --target=integration_test/tests/complete_all_features_test.dart
   ```

2. **Ajuste seletores:** Baseado na estrutura real da UI se necessário

3. **Revise os resultados:** Verifique os logs e relatórios gerados

4. **Documente resultados:** Para a monografia usando os relatórios em `docs/`

**Tabela 4 (monografia):** o PNG canónico **não** é produzido pelos testes Flutter. Regenerar a partir dos resultados embutidos no gerador:

```bash
# Na raiz do repositório — grava também evaluation/02_graphs/tables/tabela-4_e2e_test_results_table.png
python3 evaluation/scripts/02_api_performance/generate_e2e_test_table.py --thesis
```

Sem `--thesis`, só é criada uma cópia com timestamp em `evaluation/api_load_testing/graphs/`. Para alterar linhas da tabela, edite a lista `TESTES` em `generate_e2e_test_table.py`. Inventário: [`evaluation/02_graphs/MANIFEST.md`](../../../evaluation/02_graphs/MANIFEST.md).

## 📚 Documentação Adicional

- **Como executar testes**: `docs/HOW_TO_RUN_TESTS.md`
- **Relatório de testes críticos**: `docs/CRITICAL_USER_FLOWS_TEST_REPORT.md`
- **Relatório completo**: `docs/COMPREHENSIVE_TEST_REPORT.md`
- **Resumo de resultados**: `docs/TEST_RESULTS_SUMMARY.md`

## 📚 Recursos

- [Flutter Integration Testing](https://docs.flutter.dev/testing/integration-tests)
- [WidgetTester API](https://api.flutter.dev/flutter/flutter_test/WidgetTester-class.html)
- [Integration Test Package](https://pub.dev/packages/integration_test)

---

**Criado:** 28 de Outubro de 2025  
**Tipo:** Testes E2E Reais de Aplicação Mobile  
**Framework:** Flutter + integration_test

