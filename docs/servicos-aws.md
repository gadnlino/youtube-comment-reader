# Serviços da AWS e tecnologias utilizados

Este documento lista os serviços da AWS e as principais tecnologias empregados na camada intermediária (API *proxy*) da aplicação, com uma breve descrição da responsabilidade de cada um. Os componentes de execução também estão representados no diagrama de arquitetura física (Figura 22 da monografia).

| Serviço / Tecnologia | Responsabilidade na aplicação |
|----------------------|-------------------------------|
| Amazon API Gateway   | Expõe os *endpoints* HTTP e roteia cada requisição para a função Lambda correspondente. |
| AWS Lambda           | Executa, de forma *serverless*, a lógica de negócio (busca de vídeos, comentários, respostas e análise de sentimentos). |
| Amazon DynamoDB      | *Cache* distribuído das respostas da YouTube Data API, reduzindo chamadas externas e latência. |
| AWS Secrets Manager  | Armazena valores confidenciais, como chaves da API do YouTube e credenciais. |
| AWS SDK              | Permite que as funções Lambda interajam com os demais serviços da AWS. |
| AWS CDK              | Define a infraestrutura como código (*Infrastructure as Code*). |
| Amazon CloudWatch    | Coleta métricas e *logs* de cada função para observabilidade. |
| AWS X-Ray            | Rastreamento distribuído (*tracing*) das requisições entre componentes. |
| TypeScript           | Linguagem de implementação das funções Lambda. |
