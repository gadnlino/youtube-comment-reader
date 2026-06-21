# Datasets para Validação Independente do Modelo

> **Objetivo**: Encontrar datasets de comentários do YouTube ou outras redes sociais que possam ser usados para validação independente, com vídeos/comentários que **não** estavam no dataset original usado para treinamento.

---

## 📊 Dataset Atual Utilizado

**Dataset**: `amaanpoonawala/youtube-comments-sentiment-dataset` (Kaggle)
- **Fonte**: Kaggle via `kagglehub`
- **Tamanho**: 1.032.225 comentários
- **Formato**: CSV com colunas: VideoID, VideoTitle, CommentText, Sentiment
- **Classes**: Positive, Negative, Neutral

---

## 🔍 Resultados da Busca

### ✅ Datasets de Comentários do YouTube (Descobertos!)

**Boa Notícia**: Encontrei datasets de comentários do YouTube que podem ser diferentes do dataset atual!

#### **1. YTCommentVerse** 🎯 **MUITO PROMISSOR**
- **Tamanho**: 32+ milhões de comentários de 178.000 vídeos
- **Categorias**: 15 categorias distintas (Música, Notícias, Educação, Entretenimento, etc.)
- **Idiomas**: Mais de 50 idiomas
- **Metadados**: IDs de vídeo, canal, curtidas, categoria
- **Vantagem**: ✅ Grande variedade de temas/categorias, ✅ Comentários do YouTube, ✅ Multilíngue
- **Desvantagem**: ⚠️ Pode não ter ground truth de sentimento explícito (precisa verificar)
- **Link**: [arXiv:2509.11057](https://arxiv.org/abs/2509.11057)

#### **2. AmaanP314/youtube-comment-sentiment** (Hugging Face) ✅
- **Tamanho**: 1+ milhão de comentários
- **Labels**: Positivo, Neutro, Negativo
- **Tópicos**: Programação, notícias, esportes, política e mais
- **Vantagem**: ✅ Tem ground truth de sentimento, ✅ Variedade de tópicos, ✅ Comentários do YouTube
- **Desvantagem**: ⚠️ Pode ser o mesmo dataset que você já usa (precisa verificar se é diferente)
- **Link**: [Hugging Face](https://huggingface.co/datasets/AmaanP314/youtube-comment-sentiment)

#### **3. YT-30M**
- **Tamanho**: 32+ milhões de comentários
- **Categorias**: Múltiplas categorias (Notícias e Política, Ciência e Tecnologia, etc.)
- **Vantagem**: ✅ Grande volume, ✅ Variedade de categorias
- **Desvantagem**: ⚠️ Pode não ter ground truth de sentimento
- **Link**: [arXiv:2412.03465](https://arxiv.org/abs/2412.03465)

---

## ✅ Alternativas Encontradas

### 1. Datasets de Outras Redes Sociais (Texto)

#### **Twitter Sentiment Analysis Datasets** ✅ (COM GROUND TRUTH)

**1. sentiment140**
- **Tamanho**: ~1.6M tweets
- **Labels**: 0 (negativo), 2 (neutro), 4 (positivo)
- **Formato**: CSV com colunas: sentiment, id, date, query, user, text
- **Fonte**: Stanford (via Kaggle)
- **Variabilidade de Temas**: 
  - ✅ Tem coluna "query" (termo de busca usado para coletar)
  - ✅ Muitos tweets têm "NO_QUERY" (tweets gerais, não filtrados)
  - ✅ Coletado em fevereiro de 2009 (período específico)
  - ⚠️ Rotulado automaticamente com base em emoticons (pode ter viés)
  - ⚠️ Não há informação específica sobre variedade de temas nas queries
- **Vantagem**: Grande volume, labels claros
- **Desvantagem**: Rotulação automática (emoticons), pode não ter tanta variedade de temas
- **Link**: Kaggle - "Sentiment140 dataset with 1.6 million tweets"

**2. Twitter US Airline Sentiment** ✅
- **Tamanho**: ~14.000 tweets
- **Labels**: positive, negative, neutral
- **Formato**: CSV com coluna `airline_sentiment`
- **Fonte**: Kaggle
- **Vantagem**: Labels explícitos (positive/negative/neutral), similar ao YouTube
- **Link**: Kaggle - "Twitter US Airline Sentiment"

**3. SemEval-2017 Task 4: Sentiment Analysis in Twitter**
- **Tamanho**: Varia por subtarefa
- **Labels**: positive, negative, neutral (alguns com intensidade)
- **Formato**: TSV/CSV
- **Fonte**: SemEval competition
- **Vantagem**: Dataset de competição, bem anotado
- **Link**: SemEval website

**4. Tweets em Português - Análise de Sentimentos** ✅
- **Tamanho**: 2.787 tweets
- **Labels**: positivo, negativo, neutro
- **Formato**: Dataset específico
- **Fonte**: Repositório UFPB
- **Vantagem**: Em português, similar ao contexto do YouTube
- **Link**: [repositorio.ufpb.br](https://repositorio.ufpb.br/jspui/handle/123456789/28793)

**5. Hugging Face - tweets_pt_sentiment_analysis** ✅
- **Tamanho**: Varia
- **Labels**: Sentimentos anotados
- **Formato**: Hugging Face dataset
- **Fonte**: Hugging Face
- **Vantagem**: Fácil de usar, em português
- **Link**: [huggingface.co/datasets/ricardo-filho/tweets_pt_sentiment_analysis](https://huggingface.co/datasets/ricardo-filho/tweets_pt_sentiment_analysis)

**Desvantagem**: Formato diferente (tweets vs comentários de vídeo), mas similar em estrutura
**Uso**: Pode validar se o modelo generaliza para texto de redes sociais em geral

#### **Reddit Comments Sentiment**
- **Vantagem**: Comentários similares ao YouTube
- **Exemplos**:
  - `Reddit Comments Dataset` (Kaggle)
  - `r/all comments` datasets
- **Desvantagem**: Pode não ter ground truth de sentimento
- **Uso**: Similar ao YouTube, mas contexto diferente

#### **Instagram Comments**
- **Vantagem**: Similar ao YouTube (comentários em posts)
- **Desvantagem**: Datasets públicos são raros
- **Uso**: Validação em contexto similar

### 2. Datasets de Comentários de Aplicativos (Português)

#### **Dataset Anotado de Sentimentos - Comentários de Aplicativos Móveis**
- **Fonte**: SBC - Dataset em português brasileiro
- **Tamanho**: 3.000 avaliações
- **Classes**: 7 emoções básicas
- **Vantagem**: Em português, similar ao contexto de comentários
- **Desvantagem**: Pequeno tamanho, contexto diferente (app reviews vs vídeos)
- **Link**: [sol.sbc.org.br](https://sol.sbc.org.br/index.php/dsw/article/view/30616)

### 3. Datasets de Análise de Sentimento em Geral

#### **IMDB Reviews (Traduzido para Português)**
- **Vantagem**: Grande volume, traduzido para português
- **Desvantagem**: Contexto muito diferente (reviews de filmes vs comentários de vídeo)
- **Uso**: Validação de capacidade de generalização para texto em português

#### **Amazon Product Reviews**
- **Vantagem**: Grande volume, múltiplos idiomas
- **Desvantagem**: Contexto diferente
- **Uso**: Validação de generalização para texto de reviews

---

## 💡 Recomendações

### Opção 1: Usar Dataset de Twitter (Mais Prático) ✅ RECOMENDADO

**Vantagens**:
- ✅ Similar ao YouTube (texto curto, linguagem informal)
- ✅ Grande volume disponível
- ✅ **Tem ground truth de sentimentos** (positive/negative/neutral)
- ✅ Fácil de obter
- ✅ Valida generalização para redes sociais em geral
- ✅ Pode usar dataset em português (tweets_pt_sentiment_analysis)

**Datasets Recomendados**:
1. **Twitter US Airline Sentiment** (Kaggle) - Labels explícitos: positive/negative/neutral
2. **tweets_pt_sentiment_analysis** (Hugging Face) - Em português
3. **sentiment140** (Kaggle) - Grande volume (1.6M tweets)

**Implementação**:
1. Baixar dataset de sentiment do Twitter (ex: `Twitter US Airline Sentiment`)
2. Adaptar script de validação para trabalhar com formato do Twitter
3. Mapear labels do Twitter para formato do modelo (Positive/Negative/Neutral)
4. Executar validação e comparar métricas

**Script necessário**: Criar `validate_with_twitter_dataset.py`

### Opção 2: Criar Dataset Próprio (Mais Trabalhoso, Mas Mais Válido)

**Vantagens**:
- ✅ Vídeos completamente novos
- ✅ Comentários novos (coletados agora)
- ✅ Garantia de que não há sobreposição
- ✅ Validação verdadeiramente independente

**Implementação**:
1. Selecionar vídeos do YouTube que **não** estão no dataset original
2. Coletar comentários via API do YouTube
3. Anotar manualmente uma amostra (ou usar modelo de referência)
4. Validar modelo nesses comentários

**Script necessário**: Criar `validate_with_new_videos.py`

### Opção 3: Usar Dataset de Reddit (Meio Termo)

**Vantagens**:
- ✅ Comentários similares ao YouTube
- ✅ Contexto diferente (Reddit vs YouTube)
- ✅ Valida generalização para comentários em geral

**Desvantagens**:
- ⚠️ Pode não ter ground truth de sentimento
- ⚠️ Pode precisar anotar manualmente

---

## 🎯 Recomendação Final

**Para validação mais robusta, recomendo** (em ordem de prioridade):

### 1. **YTCommentVerse ou AmaanP314/youtube-comment-sentiment** 🥇 **MELHOR OPÇÃO**
   - ✅ **Comentários do YouTube** (mesmo contexto do modelo)
   - ✅ **Variedade de temas/categorias** (15 categorias no YTCommentVerse)
   - ✅ **Ground truth de sentimentos** (AmaanP314 tem labels)
   - ✅ **Dataset independente** (provavelmente diferente vídeos/comentários)
   - ⚠️ **Ação necessária**: Verificar se AmaanP314 é diferente do dataset atual
   - **Próximo passo**: Verificar disponibilidade e formato desses datasets

### 2. **Twitter US Airline Sentiment** 🥈 **SEGUNDA MELHOR OPÇÃO**
   - ✅ **Tem ground truth de sentimentos** (positive/negative/neutral)
   - ✅ Implementação rápida
   - ✅ Valida generalização para redes sociais
   - ✅ Dataset completamente independente do YouTube
   - ⚠️ **Limitação**: Tema específico (companhias aéreas), menos variabilidade

### 3. **sentiment140** 🥉 **TERCEIRA OPÇÃO**
   - ✅ Grande volume (1.6M tweets)
   - ✅ Tem coluna "query" (alguma variedade de temas)
   - ✅ Muitos tweets com "NO_QUERY" (tweets gerais)
   - ⚠️ **Limitação**: Rotulação automática (emoticons), pode ter menos variedade de temas
   - ⚠️ **Limitação**: Coletado em 2009 (dados antigos)

### 4. **Criar Dataset Próprio** (Médio Prazo)
   - Validação verdadeiramente independente
   - Vídeos que não estavam no dataset original
   - Mais trabalho, mas mais válido

### 5. **Documentação**: Atualizar argumentos de generalização
   - Ser transparente sobre limitações atuais
   - Documentar que vídeos são do mesmo dataset, mas selecionados aleatoriamente
   - Adicionar nota sobre validação com dataset independente

---

## 📝 Próximos Passos Sugeridos

1. **Verificar disponibilidade de datasets de Twitter**:
   ```bash
   # Verificar datasets no Kaggle
   # Verificar datasets no Hugging Face
   ```

2. **Criar script de validação com dataset externo**:
   - `validate_with_external_dataset.py`
   - Aceitar diferentes formatos de dataset
   - Comparar métricas com benchmark

3. **Atualizar documentação**:
   - Adicionar seção sobre validação com dataset independente
   - Documentar limitações da validação atual
   - Adicionar resultados quando disponíveis

---

## 🔗 Links Úteis

- **Kaggle Datasets**: https://www.kaggle.com/datasets
- **Hugging Face Datasets**: https://huggingface.co/datasets
- **Google Dataset Search**: https://datasetsearch.research.google.com/
- **Papers with Code Datasets**: https://paperswithcode.com/datasets

---

**Última Atualização**: Novembro 2025  
**Status**: 🔍 Busca Inicial Realizada - Recomendações Documentadas

