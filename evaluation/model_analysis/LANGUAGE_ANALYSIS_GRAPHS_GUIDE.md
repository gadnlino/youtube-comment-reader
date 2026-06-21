# Gráficos de Análise Multilíngue - Guia de Inserção

> **Arquivado (2026-06):** Os PNGs listados abaixo **não** fazem parte do conjunto canônico da monografia (docx). Foram movidos para [`evaluation/06_archived/pruned_figures/2026-06/`](../06_archived/pruned_figures/2026-06/). Figuras oficiais: [`evaluation/02_graphs/MANIFEST.md`](../02_graphs/MANIFEST.md). O script `generate_language_analysis_graphs.py` permanece executável; novas saídas não entram no keep-list.

## 📊 Gráficos Gerados para a Monografia

Este documento lista todos os gráficos gerados pela análise multilíngue de viés linguístico no modelo de classificação de sentimento.

---

## 1. **language_neutral_bias_comparison_20251102_125322.png**

**Título sugerido**: "Figura X - Comparação da Taxa Média de Classificação NEUTRAL por Idioma"

**Legenda detalhada**:
> Comparação estatística da taxa média de classificação como sentimento NEUTRAL entre diferentes idiomas. As barras mostram a média percentual com barras de erro representando o desvio padrão (quando aplicável). A linha pontilhada azul indica o baseline de performance em inglês (71,8%). Observa-se viés linguístico significativo para português (+14,2 pp) e coreano/multilíngue (+8,2 pp), enquanto espanhol apresenta performance próxima ao baseline devido à alta variabilidade intra-idioma.

**Onde inserir**: Logo após a primeira menção ao estudo multilíngue expandido.

**Resultados mostrados**:
- Inglês (baseline): 71,8% ± 8,2%
- Espanhol: 70,0% ± 32,5%
- Português: 86,0% (sem desvio - apenas 1 vídeo)
- Coreano/Multi: 80,0% (sem desvio - apenas 1 vídeo)

---

## 2. **individual_video_neutral_rates_20251102_125322.png**

**Título sugerido**: "Figura X - Taxa de Classificação NEUTRAL por Vídeo Individual"

**Legenda detalhada**:
> Distribuição individual da taxa de classificação NEUTRAL para cada um dos 9 vídeos testados, organizados por idioma primário. Cada barra horizontal representa um vídeo específico, colorida por idioma (azul=inglês, laranja=espanhol, roxo=português, vermelho=coreano/multi). Destaca-se a extrema variabilidade intra-idioma no espanhol: Waka Waka (47%, Copa do Mundo) vs Despacito (93%, pior caso observado). Esta variação sugere que fatores contextuais (audiência internacional, eventos globais, bilinguismo de comentários) influenciam a performance além do idioma per se.

**Onde inserir**: Após discussão sobre variabilidade extrema do espanhol.

**Casos notáveis mostrados**:
- **Melhor**: Waka Waka (47% - espanhol/inglês bilíngue)
- **Pior**: Despacito (93% - espanhol monolíngue)
- **Inglês mais baixo**: Queen - Bohemian Rhapsody (58%)
- **Inglês mais alto**: Passenger - Let Her Go (80%)

---

## 3. **sentiment_distribution_heatmap_20251102_125322.png**

**Título sugerido**: "Figura X - Mapa de Calor da Distribuição Completa de Sentimentos"

**Legenda detalhada**:
> Heatmap mostrando a distribuição percentual completa das três classes de sentimento (POSITIVO, NEGATIVO, NEUTRAL) para todos os 9 vídeos testados. Cores verdes indicam altas percentagens, vermelhas indicam baixas percentagens. Observa-se que a linha NEUTRAL (terceira linha) apresenta predominância de cores verdes/amarelas, especialmente em vídeos não-ingleses, confirmando o viés de classificação neutra. Notavelmente, Waka Waka apresenta distribuição mais equilibrada com 37% de comentários negativos, sugerindo polarização de opinião sobre o evento esportivo.

**Onde inserir**: Como visualização complementar da distribuição de sentimentos.

**Insights visuais**:
- Predominância de verde na linha NEUTRAL (especialmente Despacito: 93%)
- Waka Waka: distribuição atípica com 37% NEGATIVE (polarização)
- Queen: maior taxa de POSITIVE (35%) entre todos os vídeos

---

## 4. **language_bias_boxplot_20251102_125322.png**

**Título sugerido**: "Figura X - Distribuição Estatística de Classificação NEUTRAL por Idioma"

**Legenda detalhada**:
> Box plot mostrando a distribuição estatística da taxa de classificação NEUTRAL agrupada por idioma. Cada box representa o intervalo interquartil (IQR), a linha vermelha indica a mediana, o diamante verde indica a média, e os pontos individuais representam os vídeos testados. Os notches nos boxes indicam intervalos de confiança de 95% para a mediana. Inglês (5 vídeos) apresenta maior dispersão estatística (IQR ≈ 20%), enquanto português e coreano têm apenas um ponto de dados cada. A sobreposição parcial dos boxes de inglês e espanhol confirma similaridade estatística entre essas distribuições, enquanto português se posiciona significativamente acima.

**Onde inserir**: Como análise estatística complementar, após discussão dos resultados médios.

**Elementos estatísticos**:
- **Inglês**: Mediana ≈ 76%, média 71,8%, IQR [68-80%]
- **Espanhol**: Grande variação (outliers em 47% e 93%)
- **Português**: Ponto único em 86%
- **Coreano/Multi**: Ponto único em 80%

---

## 📋 Ordem de Inserção Recomendada no Texto

1. **Primeiro**: `language_neutral_bias_comparison_20251102_125322.png` (overview geral)
2. **Segundo**: `individual_video_neutral_rates_20251102_125322.png` (detalhamento por vídeo)
3. **Terceiro**: `sentiment_distribution_heatmap_20251102_125322.png` (distribuição completa)
4. **Quarto**: `language_bias_boxplot_20251102_125322.png` (análise estatística aprofundada)

---

## 🎓 Pontos para Enfatizar na Apresentação

1. **Viés Linguístico Comprovado**: +14,2 pp para português, +8,2 pp para coreano
2. **Variabilidade Intra-Idioma**: Espanhol varia 46 pontos percentuais (47%-93%)
3. **Caso Extremo Documentado**: Despacito com 93% NEUTRAL
4. **Caso de Sucesso**: Waka Waka com 47% NEUTRAL (bilinguismo + contexto global)
5. **Implicações Práticas**: Sistema adequado para audiências anglófonas, limitado para mercados globais

---

## ✅ Checklist de Qualidade

- [x] Resolução 300 DPI (qualidade de impressão)
- [x] Legendas de eixos claras e em fonte legível
- [x] Cores distintas e acessíveis (colorblind-friendly)
- [x] Valores numéricos explícitos nas visualizações
- [x] Títulos descritivos e informativos
- [x] Dados fonte: 900 comentários analisados em 9 vídeos
- [x] Timestamp: 20251102_125322 (2 de novembro de 2025, 12:53:22)

---

**Data de geração**: 2 de novembro de 2025  
**Script**: `generate_language_analysis_graphs.py`  
**Dados fonte**: `multilingual_sentiment_results_20251102_125322.json`

