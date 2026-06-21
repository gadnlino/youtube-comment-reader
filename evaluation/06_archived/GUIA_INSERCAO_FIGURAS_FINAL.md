# Guia Final de Inserção de Figuras na Monografia

**Versão Simplificada em Português**  
**Data:** 2 de Novembro de 2025

---

## 📊 Total de Figuras: 9 imagens

Todas as figuras estão em **alta resolução (300 DPI)** e prontas para inserção em documentos acadêmicos.

---

## 🎯 Pilar 1: Acurácia do Modelo de Classificação de Sentimento

### Figura 1.1 - Comparação de Viés Linguístico
**Arquivo:** `comparacao_viés_neutral_idiomas_pt_20251102_125322.png`  
**Localização no texto:** Logo após a introdução da seção "Limitações relacionadas ao idioma dos comentários"  
**Legenda sugerida:**
> **Figura X:** Comparação da taxa média de classificação NEUTRAL por idioma, evidenciando viés linguístico do modelo TF-IDF. Vídeos em português apresentam +14,2 pontos percentuais de classificação neutra em relação ao baseline inglês (71,8%), enquanto vídeos coreanos/multilíngues apresentam +8,2 pp.

---

### Figura 1.2 - Taxa NEUTRAL por Vídeo Individual
**Arquivo:** `taxa_neutral_videos_individuais_pt_20251102_125322.png`  
**Localização no texto:** Após discussão sobre variabilidade extrema em espanhol  
**Legenda sugerida:**
> **Figura X:** Taxa de classificação NEUTRAL por vídeo individual, revelando variabilidade intra-idioma. Destaque para extremos em espanhol: *Waka Waka* (47,0% NEUTRAL) vs *Despacito* (93,0% NEUTRAL), diferença de 46 pontos percentuais.

---

### Figura 1.3 - Mapa de Calor de Distribuição de Sentimentos
**Arquivo:** `heatmap_distribuicao_sentimentos_pt_20251102_125322.png`  
**Localização no texto:** Complementar à análise de distribuição de sentimentos  
**Legenda sugerida:**
> **Figura X:** Mapa de calor da distribuição completa de sentimentos (positivo, negativo, neutro) em todos os vídeos testados. A visualização evidencia a predominância de classificação neutra em vídeos não-anglófonos, especialmente *Despacito* (93% neutral) e *Envolver* (86% neutral).

---

### Figura 1.4 - Box Plot Estatístico de Viés Linguístico
**Arquivo:** `boxplot_viés_linguistico_pt_20251102_125322.png`  
**Localização no texto:** Após análise estatística detalhada do viés linguístico  
**Legenda sugerida:**
> **Figura X:** Box plot estatístico mostrando distribuição de percentual NEUTRAL por idioma, incluindo pontos individuais, mediana e média. Português brasileiro apresentou o maior impacto negativo (+14,2 pp), seguido por coreano/multilíngue (+8,2 pp). Espanhol apresenta alta variabilidade (σ=32,5%) devido a fatores contextuais.

---

## 🚀 Pilar 2: Tempo de Resposta e Confiabilidade da API

### Figura 2.1 - Dashboard Executivo (mantido em inglês)
**Arquivo:** `executive_summary_dashboard.png`  
**Localização no texto:** Logo após introdução da avaliação de performance (Pilar 2)  
**Legenda sugerida:**
> **Figura X:** Dashboard executivo consolidando métricas de performance do teste multi-vídeo: tempo médio de resposta (430ms), taxa de sucesso (100%), distribuições estatísticas e comparações entre tipos de vídeo.

---

### Figura 2.2 - Box Plots de Tempo de Resposta
**Arquivo:** `boxplot_tempo_resposta_pt.png`  
**Localização no texto:** Após descrição dos três vídeos selecionados para o teste  
**Legenda sugerida:**
> **Figura X:** Box plots comparando distribuição de tempos de resposta entre os três tipos de vídeo testados. Documentário apresentou melhor consistência (mediana 368ms, σ=133ms), seguido por música viral (408ms) e vídeo musical (514ms incluindo *cold start*).

---

### Figura 2.3 - Comparação de Tempos Médios
**Arquivo:** `comparacao_tempo_medio_resposta_pt.png`  
**Localização no texto:** Após análise quantitativa dos resultados por vídeo  
**Legenda sugerida:**
> **Figura X:** Comparação de tempo médio de resposta com barras de erro (desvio padrão) entre os três vídeos testados. Diferença de apenas 27ms (7,3%) entre melhor e pior desempenho (excluindo *cold start*), confirmando independência de tipo de conteúdo.

---

### Figura 2.4 - Tendências de Tempo de Resposta Consolidadas
**Arquivo:** `tendencias_por_video_pt.png`  
**Localização no texto:** Após discussão dos três vídeos e análise de consistência  
**Legenda sugerida:**
> **Figura X:** Tendências de tempo de resposta para cada vídeo ao longo de 20 requisições. Três painéis consolidados demonstram consistência de performance após primeira requisição (*cold start*), com estabilização em níveis previsíveis independentemente do tipo de conteúdo.

---

## 📱 Pilar 3: Corretude da Navegação End-to-End

### Figura 3.1 - Tabela de Resultados dos Testes E2E
**Arquivo:** `e2e_test_results_table_20251102.png`  
**Localização no texto:** Após introdução dos 8 fluxos críticos de usuário  
**Legenda sugerida:**
> **Tabela 1:** Resultados completos dos 8 testes end-to-end da aplicação mobile Flutter, incluindo fluxo testado, funcionalidade validada, ações simuladas, resultado e tempo de execução. Taxa de sucesso: 100% (8 de 8 testes aprovados), tempo total: 2min15s, ~15 chamadas à API REST, ~30+ interações de UI simuladas.

---

## 📂 Localização dos Arquivos

Todos os arquivos PNG estão em:
```
/Users/guiavenas/source/repos/youtube-comment-reader/evaluation/api_load_testing/
```

---

## ✅ Checklist de Inserção no Word/DOCX

### Antes de Inserir:
- [ ] Abrir o documento da monografia em Word
- [ ] Localizar a seção "AVALIAÇÃO" (Capítulo 5)
- [ ] Identificar os placeholders **[INSERIR FIGURA: ...]** no texto

### Durante a Inserção:
- [ ] Inserir cada figura no local exato indicado pelo placeholder
- [ ] Aplicar a legenda sugerida (ajustar numeração sequencial)
- [ ] Centralizar a imagem na página
- [ ] Verificar que a resolução está adequada (300 DPI)
- [ ] Ajustar tamanho se necessário (manter proporção)

### Após a Inserção:
- [ ] Remover os placeholders **[INSERIR FIGURA: ...]**
- [ ] Revisar numeração sequencial das figuras (Figura 1, 2, 3...)
- [ ] Atualizar referências no texto se houver ("conforme Figura X...")
- [ ] Verificar que todas as legendas estão formatadas consistentemente
- [ ] Gerar índice de figuras automaticamente (se aplicável)

---

## 🎨 Formatação Recomendada no Word

### Para Figuras:
- **Alinhamento:** Centralizado
- **Quebra de texto:** Em linha com o texto (ou "Quadrado" se preferir)
- **Largura:** Ajustar para ocupar 80-90% da largura da página
- **Manter proporção:** Sim (sempre)

### Para Legendas:
- **Fonte:** Mesma do texto principal (geralmente Times New Roman 12pt)
- **Estilo:** Negrito para "Figura X:" ou "Tabela X:", normal para o resto
- **Alinhamento:** Justificado ou centralizado (consistente em todo documento)
- **Espaçamento:** 6pt antes, 12pt depois

---

## 📞 Troubleshooting

### Problema: Imagem aparece "borrada" no Word
**Solução:** 
1. Clique com botão direito na imagem → Formato da Imagem
2. Aba "Tamanho" → Desmarcar "Bloquear taxa de proporção"
3. Redefinir para 100% (largura e altura)
4. Verificar se a opção "Compactar imagens" está DESATIVADA

### Problema: Imagem com tamanho muito grande/pequeno
**Solução:**
1. Selecionar a imagem
2. Manter Shift pressionado
3. Arrastar canto da imagem para redimensionar proporcionalmente
4. Objetivo: largura de ~15cm para documentos A4

### Problema: Legenda não aparece abaixo da figura
**Solução:**
1. Inserir > Referência > Inserir Legenda
2. Selecionar "Figura" como rótulo
3. Posição: "Abaixo do item selecionado"
4. Colar texto da legenda sugerida

---

## 📊 Resumo Estatístico das Figuras

| Pilar | Quantidade | Idioma | Resolução |
|-------|-----------|--------|-----------|
| Pilar 1 (Modelo) | 4 figuras | Português | 300 DPI |
| Pilar 2 (API) | 4 figuras | PT + 1 EN | 300 DPI |
| Pilar 3 (E2E) | 1 figura | Português | 300 DPI |
| **TOTAL** | **9 figuras** | **8 PT + 1 EN** | **300 DPI** |

---

**Última Atualização:** 2 de Novembro de 2025, 13:25  
**Status:** ✅ Todos os arquivos verificados e disponíveis

