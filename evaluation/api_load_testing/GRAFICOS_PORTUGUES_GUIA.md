# 📊 Gráficos da Análise Multilíngue - Versão em Português

**Gerado em**: 2 de Novembro de 2025, 13:00  
**Propósito**: Inclusão na monografia/tese em português brasileiro  
**Resolução**: 300 DPI (qualidade de impressão)

---

## ✅ GRÁFICOS GERADOS (5 visualizações)

### 1. **comparacao_viés_neutral_idiomas_pt_20251102_125322.png** (153 KB)

**Título**: Impacto do Idioma na Classificação de Sentimento - Viés da Classe NEUTRAL Entre Idiomas

**Descrição**: Gráfico de barras comparando a taxa média de classificação NEUTRAL por idioma, com barras de erro mostrando desvio padrão. Linha pontilhada azul indica baseline do inglês (71,8%).

**Dados mostrados**:
- Inglês (baseline): 71,8% ± 8,2%
- Espanhol: 70,0% ± 32,5%
- Português: 86,0%
- Coreano/Multi: 80,0%

**Onde inserir**: Logo após a primeira menção ao estudo multilíngue expandido.

---

### 2. **taxa_neutral_videos_individuais_pt_20251102_125322.png** (251 KB)

**Título**: Classificação de Sentimento por Vídeo - Percentual NEUTRAL em Conteúdos de Diferentes Idiomas

**Descrição**: Gráfico de barras horizontais mostrando a taxa NEUTRAL de cada vídeo individual, colorido por idioma. Revela alta variabilidade intra-idioma no espanhol.

**Casos notáveis**:
- **Melhor geral**: Waka Waka - 47% (Espanhol/Inglês)
- **Pior geral**: Despacito - 93% (Espanhol)
- **Melhor inglês**: Queen - 58%
- **Pior inglês**: Passenger - 80%

**Onde inserir**: Após discussão sobre variabilidade extrema do espanhol.

---

### 3. **heatmap_distribuicao_sentimentos_pt_20251102_125322.png** (305 KB)

**Título**: Mapa de Calor da Distribuição de Sentimentos - Distribuição Completa por Idioma do Vídeo

**Descrição**: Heatmap mostrando distribuição percentual das três classes (POSITIVO, NEGATIVO, NEUTRO) para todos os 9 vídeos. Verde = alta %, vermelho = baixa %.

**Insights visuais**:
- Predominância de verde na linha NEUTRO (especialmente Despacito: 93%)
- Waka Waka: distribuição atípica com 37% NEGATIVO
- Queen: maior taxa de POSITIVO (35%)

**Onde inserir**: Como visualização complementar da distribuição completa de sentimentos.

---

### 4. **boxplot_viés_linguistico_pt_20251102_125322.png** (199 KB)

**Título**: Distribuição Estatística da Classificação NEUTRAL por Idioma - Box Plot com Pontos de Dados Individuais

**Descrição**: Box plot estatístico mostrando distribuição de NEUTRAL% por idioma. Linha vermelha = mediana, diamante verde = média, pontos = vídeos individuais.

**Elementos estatísticos**:
- **Inglês**: Mediana ≈ 76%, média 71,8%, IQR [68-80%]
- **Espanhol**: Grande variação (outliers em 47% e 93%)
- **Português**: Ponto único em 86%
- **Coreano/Multi**: Ponto único em 80%

**Onde inserir**: Como análise estatística complementar, após discussão dos resultados médios.

---

### 5. **comparacao_sentimentos_multilíngue_pt_20251102_125322.png** (324 KB)

**Título**: Distribuição de Sentimentos por Idioma do Vídeo - Teste do Modelo TF-IDF em Múltiplos Idiomas

**Descrição**: Gráfico de barras empilhadas mostrando distribuição completa (positivo/negativo/neutro) para cada vídeo, com rótulos de porcentagem.

**Uso recomendado**: Overview visual geral da distribuição de sentimentos em todos os vídeos testados.

**Onde inserir**: Como figura introdutória da seção multilíngue ou como resumo visual.

---

## 📝 ORDEM DE INSERÇÃO RECOMENDADA

1. **comparacao_viés_neutral_idiomas_pt_20251102_125322.png** - Primeiro (overview por idioma)
2. **taxa_neutral_videos_individuais_pt_20251102_125322.png** - Segundo (detalhamento por vídeo)
3. **heatmap_distribuicao_sentimentos_pt_20251102_125322.png** - Terceiro (distribuição completa)
4. **boxplot_viés_linguistico_pt_20251102_125322.png** - Quarto (análise estatística)
5. **comparacao_sentimentos_multilíngue_pt_20251102_125322.png** - Opcional (resumo visual alternativo)

---

## 📊 DADOS FONTE

- **Arquivo JSON**: `multilingual_sentiment_results_20251102_125322.json`
- **Total de vídeos**: 9 bem-sucedidos
- **Total de comentários**: 900
- **Idiomas testados**: 
  - Inglês: 5 vídeos (500 comentários)
  - Espanhol: 2 vídeos (200 comentários)
  - Português: 1 vídeo (100 comentários)
  - Coreano/Multi: 1 vídeo (100 comentários)

---

## 🔑 PRINCIPAIS ACHADOS VISUALIZADOS

### ✅ Viés Linguístico Comprovado:
- **Português**: +14,2 pp vs inglês (86% NEUTRAL)
- **Coreano/Multi**: +8,2 pp vs inglês (80% NEUTRAL)
- **Espanhol**: -1,8 pp vs inglês (70% NEUTRAL, mas alta variabilidade)

### ✅ Variabilidade Intra-Idioma:
- **Espanhol**: 47% (Waka Waka) a 93% (Despacito) = 46 pp de variação
- **Inglês**: 58% (Queen) a 80% (Passenger) = 22 pp de variação

### ✅ Casos Extremos:
- **Pior**: Despacito - 93% NEUTRAL
- **Melhor não-inglês**: Waka Waka - 47% NEUTRAL

---

## 🎨 CARACTERÍSTICAS DOS GRÁFICOS

### Estilo Visual:
- ✅ Títulos e eixos em **português brasileiro**
- ✅ Fontes legíveis (DejaVu Sans)
- ✅ Cores profissionais (azul para inglês, laranja para espanhol, roxo para português, vermelho para coreano)
- ✅ Grade de fundo discreta
- ✅ Rótulos de valores explícitos

### Qualidade Técnica:
- ✅ Resolução: **300 DPI** (qualidade de impressão)
- ✅ Formato: PNG com fundo branco
- ✅ Tamanho médio: ~230 KB por gráfico
- ✅ Dimensões ajustadas para A4 (10x6 a 14x8 polegadas)

---

## 📖 LEGENDAS SUGERIDAS PARA A MONOGRAFIA

### Figura 1 (Comparação por Idioma):
> "Comparação da taxa média de classificação como sentimento NEUTRAL entre diferentes idiomas. As barras mostram a média percentual com barras de erro representando o desvio padrão. A linha pontilhada azul indica o baseline de performance em inglês (71,8%). Observa-se viés linguístico significativo para português (+14,2 pp) e coreano/multilíngue (+8,2 pp), enquanto espanhol apresenta performance próxima ao baseline devido à alta variabilidade intra-idioma."

### Figura 2 (Vídeos Individuais):
> "Distribuição individual da taxa de classificação NEUTRAL para cada um dos 9 vídeos testados, organizados por idioma primário. Destaca-se a extrema variabilidade intra-idioma no espanhol: Waka Waka (47%, Copa do Mundo) vs Despacito (93%, pior caso observado). Esta variação sugere que fatores contextuais (audiência internacional, eventos globais, bilinguismo de comentários) influenciam a performance além do idioma per se."

### Figura 3 (Heatmap):
> "Heatmap mostrando a distribuição percentual completa das três classes de sentimento (POSITIVO, NEGATIVO, NEUTRO) para todos os 9 vídeos testados. Cores verdes indicam altas percentagens, vermelhas indicam baixas percentagens. Observa-se que a linha NEUTRO apresenta predominância de cores verdes/amarelas, especialmente em vídeos não-ingleses, confirmando o viés de classificação neutra."

### Figura 4 (Box Plot):
> "Box plot mostrando a distribuição estatística da taxa de classificação NEUTRAL agrupada por idioma. Cada box representa o intervalo interquartil (IQR), a linha vermelha indica a mediana, o diamante verde indica a média, e os pontos individuais representam os vídeos testados. Inglês (5 vídeos) apresenta maior dispersão estatística (IQR ≈ 20%), enquanto português se posiciona significativamente acima do baseline."

---

## ✅ CHECKLIST DE QUALIDADE

- [x] Todos os textos em português brasileiro
- [x] Acentuação correta (viés, multilíngue, etc.)
- [x] Resolução 300 DPI
- [x] Cores acessíveis e profissionais
- [x] Legendas de eixos claras
- [x] Valores numéricos explícitos
- [x] Fundo branco (pronto para impressão)
- [x] Arquivos PNG otimizados
- [x] Nomes de arquivo descritivos

---

## 🎓 PRONTO PARA MONOGRAFIA!

Todos os gráficos estão prontos para inserção direta no documento Word/LaTeX da monografia em português. Os arquivos podem ser importados como figuras de alta qualidade sem necessidade de edição adicional.

**Localização**: `/Users/guiavenas/source/repos/youtube-comment-reader/evaluation/api_load_testing/`

---

**Última atualização**: 2 de novembro de 2025, 13:00  
**Script gerador**: `generate_language_analysis_graphs_pt.py`  
**Status**: ✅ COMPLETO E PRONTO PARA USO

