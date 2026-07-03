# Catálogo de Scripts

Índice dos scripts executáveis. Visão geral em [`README.md`](README.md).

Constantes de caminho: [`_paths.py`](_paths.py)

Estado da verificação: [`VERIFICATION_STATUS.md`](VERIFICATION_STATUS.md)

| Script | Categoria | Finalidade | Diretório de trabalho | Saída |
|--------|-----------|------------|----------------------|-------|
| `analyze_video_language.py` | modelo | Analisa distribuição de idiomas nos comentários de vídeos | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `compare_metrics_vs_benchmark.py` | modelo | Compara métricas da validação com o benchmark inicial | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py` | modelo | Avalia TF-IDF+LR no dataset Kaggle amitzala | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `generate_confusion_matrix.py` | modelo | Gera matriz de confusão (dados fixos, offline) | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `generate_consolidated_distribution_analysis.py` | modelo | Gráficos consolidados de distribuição de sentimentos | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `generate_language_analysis_graphs.py` | modelo | Gráficos de análise multilíngue (inglês) | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `generate_language_analysis_graphs_pt.py` | modelo | Gráficos de análise multilíngue (português) | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `generate_metrics_comparison_table.py` | modelo | Tabela comparativa benchmark vs validação | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `generate_sentiment_distribution_by_language.py` | modelo | Distribuição de sentimento por idioma | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `generate_twitter_airline_graphs.py` | modelo | Gráficos da validação Twitter Airline | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `generate_validation_graphs.py` | modelo | Gráficos a partir de resultados de validação independente | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `language_impact_analysis.py` | modelo | Impacto do idioma na classificação de sentimento | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `multilingual_sentiment_analysis.py` | modelo | Estudo multilíngue de sentimento | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `plot_tfidf_lr_selection_vs_kaggle_amitzala.py` | modelo | Compara seleção do modelo vs dataset Kaggle | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `pre_filter_working_videos.py` | modelo | Pré-filtra vídeos que funcionam com a API | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `validate_model_accuracy_with_dataset.py` | modelo | Valida acurácia com ground truth comentário a comentário | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `validate_model_distribution.py` | modelo | Valida distribuição de sentimentos (conjunto pequeno) | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `validate_model_distribution_multiple_sets.py` | modelo | Valida viés com múltiplos conjuntos de vídeos | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `validate_model_distribution_vs_benchmark.py` | modelo | Compara distribuição observada vs benchmark | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `validate_with_airespucrs_pt.py` | modelo | Validação com dataset AiresPucrs (PT) | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `validate_with_app_reviews_pt.py` | modelo | Validação com reviews de apps (PT) | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `validate_with_imdb_reviews.py` | modelo | Validação com reviews IMDB | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `validate_with_tweets_pt.py` | modelo | Validação com tweets em português | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `validate_with_twitter_airline.py` | modelo | Validação com Twitter US Airline Sentiment | `evaluation/scripts/01_model_evaluation/` | `model_analysis/results/` |
| `comments.py` | performance-api | Testes do endpoint de comentários | `evaluation/scripts/02_api_performance/` | `api_load_testing/results/` |
| `common.py` | performance-api | Utilitários HTTP, métricas e gráficos partilhados | `evaluation/scripts/02_api_performance/` | `api_load_testing/results/` |
| `generate_consolidated_graphs.py` | performance-api | Gráficos consolidados dos testes de API | `evaluation/scripts/02_api_performance/` | `api_load_testing/results/` |
| `generate_e2e_test_table.py` | performance-api | Tabela de resultados dos testes E2E | `evaluation/scripts/02_api_performance/` | `api_load_testing/results/` |
| `generate_locust_graphs.py` | performance-api | Gráficos a partir de resultados Locust | `evaluation/scripts/02_api_performance/` | `api_load_testing/results/` |
| `locust_max_tps.py` | performance-api | Teste Locust para TPS máximo | `evaluation/scripts/02_api_performance/` | `api_load_testing/results/` |
| `locust_test.py` | performance-api | Teste de carga Locust básico | `evaluation/scripts/02_api_performance/` | `api_load_testing/results/` |
| `run_all.py` | performance-api | Executa todos os testes de performance da API | `evaluation/scripts/02_api_performance/` | `api_load_testing/results/` |
| `run_max_tps_test.sh` | performance-api | Shell para teste de TPS máximo | `evaluation/scripts/02_api_performance/` | `api_load_testing/results/` |
| `stability.py` | performance-api | Teste de estabilidade temporal da API | `evaluation/scripts/02_api_performance/` | `api_load_testing/results/` |
| `videos.py` | performance-api | Testes do endpoint de vídeos | `evaluation/scripts/02_api_performance/` | `api_load_testing/results/` |
| `generate_academic_graphs.py` | performance-api | Gráficos académicos de performance (inglês) | `evaluation/scripts/02_api_performance/generators/` | `api_load_testing/` |
| `generate_academic_graphs_pt.py` | performance-api | Gráficos académicos de performance (português) | `evaluation/scripts/02_api_performance/generators/` | `api_load_testing/` |
| `batch_size_analysis.py` | performance-api | Análise do impacto do tamanho do lote | `evaluation/scripts/02_api_performance/benchmarks/` | `api_load_testing/` |
| `config_template.py` | performance-api | Modelo de configuração para benchmarks | `evaluation/scripts/02_api_performance/benchmarks/` | `api_load_testing/` |
| `extended_benchmark.py` | performance-api | Benchmark estendido (219 requisições) | `evaluation/scripts/02_api_performance/benchmarks/` | `api_load_testing/` |
| `heavy_load_test.py` | performance-api | Teste de carga pesada (~10.600 comentários) | `evaluation/scripts/02_api_performance/benchmarks/` | `api_load_testing/` |
| `locustfile.py` | performance-api | Definição Locust para load testing | `evaluation/scripts/02_api_performance/benchmarks/` | `api_load_testing/` |
| `multi_video_benchmark.py` | performance-api | Benchmark com múltiplos vídeos | `evaluation/scripts/02_api_performance/benchmarks/` | `api_load_testing/` |
| `performance_benchmark.py` | performance-api | Benchmark básico de performance | `evaluation/scripts/02_api_performance/benchmarks/` | `api_load_testing/` |
| `quick_test.py` | performance-api | Teste rápido da API | `evaluation/scripts/02_api_performance/benchmarks/` | `api_load_testing/` |
| `e2e_functionality_test.py` | e2e-api | Testes E2E da API (Python, legado) | `evaluation/scripts/03_api_e2e/` | `e2e_functionality_testing/` |
| `comprehensive_model_comparison.py` | comparacao-modelos | Comparação abrangente de modelos de sentimento | `evaluation/model_comparison/scripts/` | `model_comparison/results/` |
| `fix_nltk_ssl.py` | comparacao-modelos | Corrige SSL do NLTK para downloads | `evaluation/model_comparison/scripts/` | `model_comparison/results/` |
| `nltk_setup.py` | comparacao-modelos | Configuração do NLTK | `evaluation/model_comparison/scripts/` | `model_comparison/results/` |
| `svm_classification_report.py` | comparacao-modelos | Relatório de classificação SVM | `evaluation/model_comparison/scripts/` | `model_comparison/results/` |
| `textblob_classification_report.py` | comparacao-modelos | Relatório de classificação TextBlob | `evaluation/model_comparison/scripts/` | `model_comparison/results/` |
| `tfidf_logistic_classification_report.py` | comparacao-modelos | Relatório TF-IDF + Regressão Logística | `evaluation/model_comparison/scripts/` | `model_comparison/results/` |
| `vader_classification_report.py` | comparacao-modelos | Relatório de classificação VADER | `evaluation/model_comparison/scripts/` | `model_comparison/results/` |
| `deploy-with-sentiment.sh` | implantacao | Deploy completo do backend (Docker + ECR + CDK) | `infra/` | `n/a` |

Script arquivado (só build/push): `infra/archive/build-and-push-sentiment-image.sh` — use `deploy-with-sentiment.sh` ou `npm run deploy:dev`.

## Localizações anteriores

| Caminho anterior | Caminho canônico |
|------------------|------------------|
| `evaluation/model_analysis/scripts/` | `evaluation/scripts/01_model_evaluation/` |
| `evaluation/api_load_testing/scripts/` | `evaluation/scripts/02_api_performance/` |
| `evaluation/04_scripts/tests/` | `evaluation/scripts/02_api_performance/benchmarks/` |
| `evaluation/04_scripts/generators/` | `evaluation/scripts/02_api_performance/generators/` |
| `evaluation/e2e_functionality_testing/e2e_functionality_test.py` | `evaluation/scripts/03_api_e2e/e2e_functionality_test.py` |
| `evaluation/GUIA_COMPLETO_SCRIPTS_AVALIACAO.md` | `evaluation/scripts/CATALOG.md` |
