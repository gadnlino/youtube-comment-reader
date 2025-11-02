# Flutter Integration Tests - YouTube Comment Reader

## 📋 Visão Geral

Estes são **testes de integração E2E (end-to-end) REAIS** que simulam o comportamento do usuário na aplicação Flutter mobile. Diferente dos testes de API, estes testes:

✅ **Renderizam a interface gráfica** do Flutter  
✅ **Simulam cliques** em botões e componentes  
✅ **Digitam texto** em campos de busca  
✅ **Navegam entre telas** como um usuário real  
✅ **Verificam elementos visuais** na UI  

## 🎯 Testes Implementados

1. **Test 1:** Busca de vídeos e exibição de resultados
2. **Test 2:** Carregamento de comentários SEM análise de sentimento
3. **Test 3:** Carregamento de comentários COM análise de sentimento
4. **Test 4:** Filtragem por comentários POSITIVOS (verifica 100% de acurácia do filtro)
5. **Test 5:** Filtragem por comentários NEGATIVOS (verifica 100% de acurácia do filtro)
6. **Test 6:** Filtragem por comentários NEUTROS (verifica 100% de acurácia do filtro)
7. **Test 7:** Múltiplos filtros ativos simultaneamente
8. **Test 8:** Tratamento de erros com vídeos inválidos

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

### Opção 1: Teste Rápido (sem device)

Para testar a lógica sem renderizar em device/emulador:

```bash
cd packages/frontend
flutter test integration_test/app_test.dart
```

### Opção 2: Teste Completo (com device/emulador)

Para rodar com renderização real em device ou emulador:

```bash
cd packages/frontend

# 1. Certifique-se de que um emulador está rodando ou device conectado
flutter devices

# 2. Execute os testes
flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/app_test.dart
```

### Opção 3: Teste em Device Específico

```bash
# Listar devices disponíveis
flutter devices

# Executar em device específico
flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/app_test.dart \
  -d <device_id>
```

## 📊 Exemplo de Output Esperado

```
✅ Test 1 PASSED: Video search functionality works
✅ Test 2 PASSED: Comments load without sentiment
✅ Test 3 PASSED: Sentiment analysis works
✅ Test 4 PASSED: Positive filter works correctly (100% accuracy)
✅ Test 5 PASSED: Negative filter works correctly (100% accuracy)
✅ Test 6 PASSED: Neutral filter works correctly (100% accuracy)
✅ Test 7 PASSED: Multiple filters work correctly
✅ Test 8 PASSED: Error handling works

================================================================================
📊 FLUTTER INTEGRATION TEST SUMMARY
================================================================================
Total Tests: 8
Test Type: End-to-End Integration (Real UI Simulation)
Technology: Flutter integration_test + WidgetTester

All tests simulate real user interactions:
  ✅ Tap gestures on buttons and UI elements
  ✅ Text input in search fields
  ✅ Navigation between screens
  ✅ Sentiment filter activation/deactivation
  ✅ Comment display verification
================================================================================
```

## 🎨 O que os Testes Fazem (Tecnicamente)

### Exemplo: Teste de Filtro Positivo

```dart
// 1. Iniciar o app (renderização real)
app.main();
await tester.pumpAndSettle();

// 2. Encontrar campo de busca e digitar (simula teclado)
final searchField = find.byType(TextField).first;
await tester.enterText(searchField, 'rick astley');

// 3. Simular tap no botão de busca
await tester.tap(find.byIcon(Icons.search));
await tester.pumpAndSettle(); // Aguardar animações

// 4. Tap no primeiro vídeo da lista
await tester.tap(find.byType(GestureDetector).first);

// 5. Habilitar análise de sentimento
await tester.tap(find.byKey(const Key('sentiment_toggle')));

// 6. Tap no filtro "Positive"
await tester.tap(find.text('Positive'));

// 7. Verificar que APENAS comentários POSITIVE são exibidos
expect(find.text('NEGATIVE'), findsNothing);
expect(find.text('NEUTRAL'), findsNothing);
expect(find.text('POSITIVE'), findsWidgets);
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

### 1. **Ajustes Necessários**

Os testes podem precisar de ajustes baseados na estrutura real da UI:

- **Keys de Widgets:** Adicione `Key()` aos widgets importantes:
  ```dart
  // Exemplo no código da aplicação
  SwitchWidget(
    key: Key('sentiment_toggle'),
    onChanged: (value) => _toggleSentiment(),
  )
  ```

- **Texto de Botões:** Verifique os textos exatos dos botões
- **Estrutura de Widgets:** Ajuste seletores baseados na árvore de widgets real

### 2. **Tempo de Espera**

Os testes incluem `pumpAndSettle()` com timeouts para aguardar:
- Animações
- Requisições de API
- Carregamento de dados

Ajuste conforme necessário:
```dart
await tester.pumpAndSettle(const Duration(seconds: 5));
```

### 3. **API Real**

Os testes fazem requisições REAIS à API em produção. Certifique-se de que:
- API está online e acessível
- Credenciais/tokens estão configurados
- Arquivo `.env` está presente

## 🐛 Troubleshooting

### Problema: "Can't find widget"
**Solução:** Adicione prints para debugar:
```dart
print(tester.allWidgets.map((w) => w.runtimeType).toList());
```

### Problema: "Timeout waiting for response"
**Solução:** Aumente os timeouts:
```dart
await tester.pump(const Duration(seconds: 10));
```

### Problema: "No devices found"
**Solução:**
```bash
# Iniciar emulador
flutter emulators --launch <emulator_id>

# Ou conectar device físico e habilitar USB debugging
```

## 📝 Próximos Passos

1. **Execute os testes:** `flutter drive ...`
2. **Ajuste seletores:** Baseado na estrutura real da UI
3. **Adicione mais testes:** Conforme necessário
4. **Documente resultados:** Para a monografia

## 📚 Recursos

- [Flutter Integration Testing](https://docs.flutter.dev/testing/integration-tests)
- [WidgetTester API](https://api.flutter.dev/flutter/flutter_test/WidgetTester-class.html)
- [Integration Test Package](https://pub.dev/packages/integration_test)

---

**Criado:** 28 de Outubro de 2025  
**Tipo:** Testes E2E Reais de Aplicação Mobile  
**Framework:** Flutter + integration_test

