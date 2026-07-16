# Funções Lambda da camada intermediária

Este documento descreve cada função AWS Lambda da camada intermediária (API *proxy*) da aplicação, com sua rota ou gatilho e a responsabilidade de cada uma. As funções são definidas como código (*Infrastructure as Code*) com o AWS CDK em [`stacks/YouTubeCommentReaderBackendStack.ts`](../stacks/YouTubeCommentReaderBackendStack.ts); o código das funções em Node.js/TypeScript está em [`packages/lambdas/ycv_api/`](../packages/lambdas/ycv_api/) e [`packages/lambdas/warmup/`](../packages/lambdas/warmup/), e a função de análise de sentimentos (Python) em [`packages/lambdas/sentiment_analysis/`](../packages/lambdas/sentiment_analysis/).

Cada função segue o princípio de responsabilidade única: executa uma operação bem definida, vinculada a um *endpoint* HTTP (via Amazon API Gateway) ou a um gatilho próprio. Os componentes também estão representados no diagrama de arquitetura física (Figura 21 da monografia).

| Função | Método e rota / gatilho | Runtime | Código | Responsabilidade |
|--------|-------------------------|---------|--------|------------------|
| `searchVideos` | `GET /search` | Node.js (TypeScript) | [`ycv_api/searchVideos.ts`](../packages/lambdas/ycv_api/searchVideos.ts) | Busca vídeos por termo e filtros (palavra-chave, relevância, data). Faz duas chamadas à YouTube Data API: `search.list` (para obter os identificadores dos vídeos) e, em seguida, `videos.list` (para obter os metadados completos). |
| `listVideos` | `GET /videos` | Node.js (TypeScript) | [`ycv_api/listVideos.ts`](../packages/lambdas/ycv_api/listVideos.ts) | Retorna a listagem inicial de vídeos exibida no *feed*, sem termo de busca. |
| `fetchVideoComments` | `GET /video/comments` | Node.js (TypeScript) | [`ycv_api/fetchComments.ts`](../packages/lambdas/ycv_api/fetchComments.ts) | Obtém os comentários principais de um vídeo (nível 1 da hierarquia): texto, número de curtidas e quantidade de respostas. Retorna `403` quando o limite (cota) da YouTube Data API é atingido. Quando a requisição inclui parâmetros de filtragem por sentimento, aciona a função de análise de sentimentos. |
| `fetchVideoCommentReplies` | `GET /search/video/comment/replies` | Node.js (TypeScript) | [`ycv_api/fetchCommentReplies.ts`](../packages/lambdas/ycv_api/fetchCommentReplies.ts) | Busca as respostas encadeadas de um comentário específico (níveis 2 em diante), acionada quando o usuário expande a discussão. Também pode acionar a análise de sentimentos quando solicitado. |
| `sentimentAnalysis` | *Lambda Function URL* (`POST`) | Python (imagem Docker no Amazon ECR) | [`sentiment_analysis/handler.py`](../packages/lambdas/sentiment_analysis/handler.py) | Recebe uma lista de comentários e retorna a classificação de sentimento (positivo, neutro ou negativo) de cada um, utilizando o modelo selecionado (TF-IDF + Regressão Logística). É exposta por uma *Lambda URL* (URL pública própria, sem passar pelo API Gateway) e protegida por uma chave enviada no cabeçalho `x-api-key`. |
| `WarmUpLambdaFunction` | Agendada (Amazon EventBridge, a cada 5 min) | Node.js (TypeScript) | [`warmup/warmup_lambda.ts`](../packages/lambdas/warmup/warmup_lambda.ts) | Faz uma chamada de *ping* à função de análise de sentimentos para mantê-la "aquecida", reduzindo o tempo de inicialização a frio (*cold start*) durante o uso real. |

> Os nomes acima são os nomes lógicos das funções; ao serem provisionadas, recebem o prefixo `YoutubeCommentReaderBackend-` (ex.: `YoutubeCommentReaderBackend-searchVideos`).

## Configuração comum

- **Cache:** as funções de API consultam o Amazon DynamoDB antes de chamar a YouTube Data API; o tempo de expiração é configurável pela variável `EXPIRATION_TIME_MINUTES` (padrão atual: 10 minutos).
- **Chave da YouTube Data API:** armazenada no AWS Secrets Manager e lida pelas funções em tempo de execução.
- **Análise de sentimentos:** as funções de comentários e respostas recebem a URL da função de sentimentos (`SENTIMENT_ANALYSIS_API_URL`) e a chave (`SENTIMENT_ANALYSIS_API_KEY`) por variáveis de ambiente.
- **CORS:** cada rota do API Gateway expõe também o método `OPTIONS` para requisições *cross-origin*.
