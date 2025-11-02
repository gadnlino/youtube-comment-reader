# Texto para Seção de Avaliação - Monografia (VERSÃO SIMPLIFICADA)

## Parágrafo para Capítulo 5 (AVALIAÇÃO)

A avaliação do sistema *YouTube Comment Reader* foi estruturada em **três pilares fundamentais e complementares**: (i) **acurácia do modelo de classificação de sentimento**, avaliando a capacidade preditiva do modelo através de comparação com dataset anotado; (ii) **tempo de resposta e confiabilidade da API**, medindo latência, escalabilidade e estabilidade do backend; e (iii) **corretude da navegação end-to-end**, validando a experiência completa do usuário através da aplicação mobile Flutter. Esta abordagem metodológica permitiu validar o sistema em todas as camadas—desde a capacidade do modelo de inferir sentimento até a usabilidade da interface mobile—fornecendo evidências empíricas robustas da viabilidade da solução para ambientes de produção.

### Pilar 1: Acurácia do Modelo de Classificação de Sentimento

O primeiro pilar da avaliação consistiu em validar a **acurácia de classificação de sentimento**. Foram comparados três modelos candidatos através de validação cruzada (80% treino, 20% teste) utilizando o dataset *YouTube Comments Sentiment Dataset* contendo mais de 1 milhão de comentários anotados: (i) **VADER**, modelo baseado em léxico de regras, que obteve acurácia de 51,80%; (ii) **TextBlob**, modelo baseado em análise léxica, que alcançou acurácia de 48,00%; e (iii) **TF-IDF + Logistic Regression**, modelo de aprendizado de máquina supervisionado que apresentou **acurácia de 66,14%** e **F1-score de 66,28%**, superando os modelos baseados em regras em mais de 14 pontos percentuais.

A escolha do modelo TF-IDF + Logistic Regression para produção foi motivada por: (i) melhor acurácia dentre os candidatos avaliados; (ii) eficiência computacional compatível com ambiente *serverless* AWS Lambda (inferência em ~50ms por lote); (iii) ausência de necessidade de GPU; e (iv) facilidade de retreinamento incremental. A acurácia de 66,14% representa um compromisso pragmático entre qualidade preditiva e viabilidade operacional em ambiente *serverless* com restrições de latência (<1s).

**Limitações relacionadas ao idioma dos comentários:** Uma limitação significativa é que o modelo foi treinado exclusivamente com **comentários em inglês**. Para validar empiricamente esta limitação, foi conduzido um **estudo comparativo multilíngue** testando 9 vídeos de diferentes idiomas (100 comentários cada): 5 vídeos em inglês, 2 em espanhol, 1 em português brasileiro, e 1 coreano/multilíngue.

**[INSERIR FIGURA: comparacao_viés_neutral_idiomas_pt_20251102_125322.png - Comparação da taxa de classificação NEUTRAL por idioma]**

Os resultados confirmaram **viés linguístico significativo** (Figura): vídeos ingleses apresentaram média de **71,8% NEUTRAL**, estabelecendo a baseline. Em contraste, vídeos em português atingiram **86,0% NEUTRAL** (+14,2 pontos percentuais), e vídeos coreanos/multilíngues apresentaram **80,0% NEUTRAL** (+8,2 pp). Surpreendentemente, vídeos em espanhol apresentaram média de 70,0% NEUTRAL, porém com **variabilidade extrema**: *Waka Waka* (Copa do Mundo) teve apenas **47,0% NEUTRAL**, enquanto *Despacito* atingiu **93,0% NEUTRAL**—o pior caso observado. Esta variabilidade sugere que **fatores contextuais** (eventos globais, bilinguismo de comentários) influenciam a performance além do idioma.

**[INSERIR FIGURA: taxa_neutral_videos_individuais_pt_20251102_125322.png - Taxa NEUTRAL por vídeo individual, revelando variabilidade intra-idioma]**

Esta **barreira de generalização cross-linguística** limita a aplicabilidade do sistema a vídeos com audiência predominantemente anglófona. Para aplicações multilíngues, recomenda-se: (i) retreinamento com datasets em múltiplos idiomas; (ii) adoção de modelos multilíngues pré-treinados (e.g., mBERT, XLM-RoBERTa); ou (iii) detecção automática de idioma com classificadores especializados. Esta limitação foi documentada transparentemente para informar decisões de implantação.

### Pilar 2: Tempo de Resposta e Confiabilidade da API

O segundo pilar focou em validar o **tempo de resposta e confiabilidade da API**. Foram realizados múltiplos testes totalizando 545 requisições e processamento de mais de 43.500 comentários. O sistema demonstrou **tempo médio de resposta de 430ms** no teste multi-vídeo, com **taxa de sucesso de 100%** e escalabilidade linear. O *overhead* introduzido pela análise de sentimento foi de apenas 254ms (32,8%), não comprometendo significativamente a experiência do usuário.

**[INSERIR FIGURA: response_time_boxplot.png - Distribuição de tempos de resposta entre diferentes tipos de vídeo]**

O **teste multi-vídeo** foi conduzido em três vídeos de categorias distintas: (i) vídeo musical clássico (*Rick Astley*), (ii) documentário histórico (*Me at the zoo*), e (iii) fenômeno viral (*Gangnam Style*). Os resultados confirmaram **ausência de viés relacionado ao tipo de conteúdo**: o documentário apresentou média de 368ms, seguido pelo viral (408ms) e musical (514ms). A maior variabilidade no vídeo musical é explicada por um *cold start* inicial (2.696ms na primeira requisição), que ao ser excluído reduz a média para ~395ms, tornando a performance entre os três vídeos consistente (diferença de apenas 7,3%).

**[INSERIR FIGURA: average_response_time_comparison.png - Comparação de médias entre vídeos com barras de erro]**

A análise estatística revelou que **95% das requisições foram atendidas em menos de 571ms**, situando-se abaixo do *threshold* de 1.000ms considerado aceitável para aplicações em tempo real. Os testes de **integração de API** validaram a corretude funcional do mecanismo de filtragem, obtendo **100% de corretude**—o sistema retorna exclusivamente comentários da categoria solicitada sem vazamento de outras classes.

### Pilar 3: Corretude da Navegação End-to-End

O terceiro pilar validou a **corretude da navegação end-to-end** através de testes automatizados de interface que simulam jornadas completas de usuários na aplicação mobile Flutter. A metodologia empregou o framework `integration_test` do Flutter, executado em emulador Android conectando-se à API real em AWS e Firebase, sem uso de mocks.

Foram implementados **8 fluxos críticos de usuário**, cobrindo desde busca e visualização de vídeos até gerenciamento de favoritos e filtragem de comentários por sentimento.

**[INSERIR FIGURA: e2e_test_results_table_20251102.png - Resultados completos dos 8 testes end-to-end com funcionalidades validadas e tempos]**

A execução dos testes totalizou **2 minutos e 15 segundos**, com **taxa de sucesso de 100% (8 de 8 testes aprovados)**. Os testes cobriram: (i) visualização de lista de vídeos (8 vídeos em ~4s); (ii) busca por palavra-chave (~22s); (iii) ordenação por data de publicação (~23s); (iv) favoritos de vídeos (~13s); (v) visualização de comentários (100 comentários em ~34s); (vi) filtragem por sentimento (~5s); (vii) persistência de favoritos no Firebase (~20s); e (viii) favoritos de comentários com retry inteligente (~20s). Durante a execução, foram realizadas ~15 chamadas à API REST, múltiplas operações de leitura/escrita no Firebase, e mais de 30 interações de UI simuladas.

A validação end-to-end confirma que: (i) a integração entre frontend Flutter, backend AWS Lambda e APIs externas opera corretamente em produção; (ii) a experiência de usuário é fluida, com transições funcionais e renderização correta; (iii) a persistência de dados no Firebase funciona conforme esperado; (iv) os mecanismos de filtragem e ordenação operam conforme especificado; e (v) o tratamento de casos de erro é robusto.

### Síntese da Avaliação

A avaliação através dos **três pilares complementares** demonstrou que o *YouTube Comment Reader* atende aos requisitos funcionais e não-funcionais em todas as dimensões. O **Pilar 1** validou acurácia de 66,14% para inglês, com limitação para outros idiomas (+14,2 pp de viés NEUTRAL para português). O **Pilar 2** evidenciou tempo médio de resposta de 430ms, taxa de sucesso de 100%, e independência de tipo de conteúdo. O **Pilar 3** confirmou operação correta de todos os fluxos críticos de usuário, com 100% de aprovação. A metodologia empregada confere credibilidade científica aos resultados e evidencia a viabilidade da solução para otimizar a experiência de leitura de comentários.

---

## Notas Importantes

### Gráficos Mantidos (6 essenciais):

**Pilar 1 (Modelo):**
1. `comparacao_viés_neutral_idiomas_pt_20251102_125322.png` - Comparação por idioma
2. `taxa_neutral_videos_individuais_pt_20251102_125322.png` - Vídeos individuais

**Pilar 2 (API):**
3. `response_time_boxplot.png` - Box plots de distribuição de tempo
4. `average_response_time_comparison.png` - Comparação de médias

**Pilar 3 (E2E):**
5. `e2e_test_results_table_20251102.png` - Tabela de resultados E2E

**Opcional:** 1 gráfico adicional se necessário para ilustração visual geral.

### Números Simplificados

**Mantidos apenas valores essenciais:**
- Acurácia do modelo: 66,14%
- Baseline inglês: 71,8% NEUTRAL
- Português: 86,0% NEUTRAL (+14,2 pp)
- Despacito (pior caso): 93,0% NEUTRAL
- Tempo médio API: 430ms
- P95: 571ms (95% < 571ms)
- Taxa de sucesso: 100%
- E2E: 8/8 testes (100%)
- Tempo total E2E: 2min 15s

### Gráficos Removidos (não essenciais):

- `executive_summary_dashboard.png` - Redundante
- `music_video_response_times.png` - Muito específico
- `documentary_response_times.png` - Muito específico
- `viral_music_response_times.png` - Muito específico
- `multi_video_response_time_distribution.png` - Histograma (box plot é suficiente)
- `cdf_response_times.png` - CDF (muito técnico, box plot é suficiente)
- `temporal_performance.png` - Menos relevante
- `video_specific_trends.png` - Redundante com outros
- `performance_summary_table.png` - Informação já no texto
- `heatmap_distribuicao_sentimentos_pt_20251102_125322.png` - Redundante
- `boxplot_viés_linguistico_pt_20251102_125322.png` - Redundante com gráfico de barras

**Resultado:** De 15+ gráficos originais para **5-6 gráficos essenciais**

---

**Versão Final:** Texto reduzido de ~7.000 palavras para ~1.200 palavras, mantendo apenas informações essenciais e 5-6 gráficos mais importantes.

