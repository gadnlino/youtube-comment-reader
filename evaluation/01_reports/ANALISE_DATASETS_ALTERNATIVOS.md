# Análise de Datasets Alternativos para Validação

## 📋 Contexto

O dataset atual `tweets_pt_sentiment_analysis` (Hugging Face) possui documentação insuficiente sobre o significado dos labels:
- `label = 0` → NEGATIVE (negativo)
- `label = 1` → NEUTRAL (não-negativo, que inclui neutro e positivo)

A falta de clareza sobre o que exatamente representa cada label torna difícil interpretar os resultados da validação.

## 🔍 Opções Encontradas

### 1. Dataset ARIA - UFPB (Português) ❌ **NÃO VIÁVEL**

**Fonte**: Laboratório ARIA - Universidade Federal da Paraíba
- **Link**: [aria.ci.ufpb.br](https://aria.ci.ufpb.br/en/analise-de-sentimentos-na-lingua-portuguesa/)
- **Tamanho**: 2.787 tweets
- **Classes**: 3 classes bem definidas
  - **Positivo**
  - **Negativo**
  - **Neutro**
- **Documentação**: ✅ Bem documentado, com artigo científico associado
- **Problema Crítico**: ❌ **O dataset contém apenas IDs dos tweets, não o conteúdo textual**
- **Implicações**:
  - ❌ Seria necessário usar a API do Twitter para recuperar o conteúdo
  - ❌ Requer autenticação e credenciais da API do Twitter
  - ❌ Muitos tweets podem ter sido deletados desde a criação do dataset
  - ❌ Rate limits da API podem tornar o processo muito lento
  - ❌ Complexidade adicional significativa

**Status**: ❌ **NÃO VIÁVEL** - Não é prático usar sem acesso à API do Twitter e muitos tweets podem estar indisponíveis

---

### 2. Dataset de Avaliações de Aplicativos Móveis (Português)

**Fonte**: SBC - Dataset Showcase Workshop
- **Link**: [sol.sbc.org.br](https://sol.sbc.org.br/index.php/dsw/article/view/30616)
- **Tamanho**: 3.000 avaliações
- **Classes**: 7 emoções básicas (não é exatamente 3 classes de sentimento)
- **Contexto**: Avaliações de aplicativos da Google Play Store
- **Vantagens**:
  - ✅ Em português brasileiro
  - ✅ Bem documentado
  - ✅ Anotado manualmente por múltiplos avaliadores
- **Desvantagens**:
  - ❌ Não tem exatamente 3 classes de sentimento (tem 7 emoções)
  - ⚠️ Contexto diferente (app reviews vs tweets/comentários)
  - ⚠️ Tamanho pequeno

**Status**: ⚠️ **NÃO RECOMENDADO** - Não tem 3 classes de sentimento

---

### 3. AiresPucrs/sentiment-analysis-pt (Português)

**Fonte**: Hugging Face
- **Link**: [huggingface.co/datasets/AiresPucrs/sentiment-analysis-pt](https://huggingface.co/datasets/AiresPucrs/sentiment-analysis-pt)
- **Tamanho**: 85.027 avaliações de filmes
- **Classes**: Apenas 2 classes (`label = 0` e `label = 1`)
- **Contexto**: Avaliações de filmes
- **Vantagens**:
  - ✅ Fácil acesso via Hugging Face
  - ✅ Tamanho grande
  - ✅ Em português
- **Desvantagens**:
  - ❌ Apenas 2 classes (não tem 3 classes)
  - ⚠️ Contexto diferente (reviews de filmes vs tweets/comentários)

**Status**: ❌ **NÃO RECOMENDADO** - Apenas 2 classes

---

### 4. tweet_eval sentiment (Multi-idioma)

**Fonte**: Hugging Face
- **Link**: [huggingface.co/datasets/tweet_eval](https://huggingface.co/datasets/tweet_eval)
- **Tamanho**: ~60.000 tweets
- **Classes**: 3 classes (`label = 0`, `label = 1`, `label = 2`)
- **Idioma**: Principalmente inglês (pelos exemplos verificados)
- **Vantagens**:
  - ✅ Fácil acesso via Hugging Face
  - ✅ 3 classes
  - ✅ Tamanho adequado
  - ✅ Contexto similar (tweets)
- **Desvantagens**:
  - ⚠️ Principalmente em inglês (não português/espanhol)
  - ⚠️ Não é especificamente para validação cross-lingual

**Status**: ⚠️ **ALTERNATIVA** - Se não encontrar opção melhor em português/espanhol

---

### 5. Datasets em Espanhol

**Busca realizada**: Não encontrei datasets em espanhol bem documentados e facilmente acessíveis com 3 classes no Hugging Face ou Kaggle.

**Opções mencionadas mas não verificadas**:
- **TASS (TASS 2020/TASS 2019)**: Dataset espanhol de análise de sentimento, mas não encontrado no Hugging Face ou Kaggle de forma direta
- **pysentimiento**: Não encontrado no Hugging Face

**Status**: ❌ **NÃO ENCONTRADO** - Não há datasets em espanhol facilmente acessíveis com 3 classes

---

## 🎯 Recomendação Final

### Opção 1: Remover Validação em Português, Manter Apenas Inglês ⭐ **RECOMENDADO**

**Por quê?**
- ✅ Twitter Airline tem 3 classes bem definidas e bem documentadas
- ✅ IMDB tem 2 classes bem definidas e bem documentadas
- ✅ Ambos têm o conteúdo textual disponível diretamente
- ✅ Já temos resultados consistentes para ambos
- ✅ Não há datasets em português viáveis com conteúdo textual disponível
- ✅ A análise de generalização pode ser feita comparando diferentes contextos (tweets vs reviews) em inglês

**Próximos passos**:
1. Remover a seção de Tweets PT do relatório
2. Atualizar a análise para focar em:
   - **Generalização para diferentes contextos** (tweets informais vs reviews formais)
   - **Generalização para diferentes domínios** (companhias aéreas vs filmes)
   - Ambos em inglês, mas com variações significativas de contexto

---

### Opção 2: Buscar Dataset em Espanhol (Alternativa)

**Por quê?**
- ✅ Espanhol é uma língua românica similar ao português
- ✅ Pode demonstrar capacidade de generalização cross-lingual
- ⚠️ Ainda precisa encontrar um dataset adequado com conteúdo textual

**Próximos passos**:
1. Buscar datasets em espanhol com conteúdo textual disponível
2. Verificar se têm 3 classes bem definidas
3. Se encontrar, adaptar o script de validação

---

## 📝 Conclusão

**Recomendação Final**: ⭐ **Remover a validação em português e manter apenas os datasets em inglês (Twitter Airline e IMDB)**

**Razões**:
1. ❌ **Dataset ARIA não é viável**: Contém apenas IDs, requer API do Twitter, muitos tweets podem estar deletados
2. ❌ **Não há outros datasets em português viáveis**: Todos os encontrados têm problemas (apenas 2 classes, sem conteúdo textual, documentação insuficiente)
3. ✅ **Datasets em inglês são adequados**: Twitter Airline e IMDB são bem documentados, têm conteúdo textual disponível, e já temos resultados consistentes
4. ✅ **Análise de generalização ainda é válida**: Podemos demonstrar generalização para:
   - **Diferentes contextos** (tweets informais vs reviews formais)
   - **Diferentes domínios** (companhias aéreas vs filmes)
   - **Diferentes formatos de texto** (curto vs longo)

**Vantagem de manter apenas inglês**: 
- Ambos os datasets (Twitter Airline e IMDB) são bem documentados
- Já temos resultados consistentes
- A análise de generalização pode ser feita comparando diferentes contextos e domínios, mesmo que todos sejam em inglês
- Evita problemas de interpretação devido à falta de documentação adequada

---

## 🔗 Links de Referência

1. **Dataset ARIA - UFPB**: [aria.ci.ufpb.br](https://aria.ci.ufpb.br/en/analise-de-sentimentos-na-lingua-portuguesa/)
2. **Dataset de Avaliações de Apps**: [sol.sbc.org.br](https://sol.sbc.org.br/index.php/dsw/article/view/30616)
3. **AiresPucrs/sentiment-analysis-pt**: [huggingface.co/datasets/AiresPucrs/sentiment-analysis-pt](https://huggingface.co/datasets/AiresPucrs/sentiment-analysis-pt)
4. **tweet_eval**: [huggingface.co/datasets/tweet_eval](https://huggingface.co/datasets/tweet_eval)

---

**Data da Análise**: 23 de Novembro de 2025

