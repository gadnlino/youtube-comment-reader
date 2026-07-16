# Serviços da AWS e tecnologias utilizados

Este documento lista os serviços da AWS e as principais tecnologias empregados na camada intermediária (API *proxy*) da aplicação, com uma breve descrição da responsabilidade de cada um. Os componentes de execução também estão representados no diagrama de arquitetura física (Figura 21 da monografia).

| Serviço / Tecnologia | Responsabilidade na aplicação | Documentação |
|----------------------|-------------------------------|--------------|
| Amazon API Gateway   | Expõe os *endpoints* HTTP e roteia cada requisição para a função Lambda correspondente. | https://docs.aws.amazon.com/apigateway/ |
| AWS Lambda           | Executa, de forma *serverless*, a lógica de negócio (busca de vídeos, comentários, respostas e análise de sentimentos). | https://docs.aws.amazon.com/lambda/ |
| Amazon DynamoDB      | *Cache* distribuído das respostas da YouTube Data API, reduzindo chamadas externas e latência. | https://docs.aws.amazon.com/dynamodb/ |
| AWS Secrets Manager  | Armazena valores confidenciais, como chaves da API do YouTube e credenciais. | https://docs.aws.amazon.com/secretsmanager/ |
| AWS SDK              | Permite que as funções Lambda interajam com os demais serviços da AWS. | https://aws.amazon.com/sdk-for-javascript/ |
| AWS CDK              | Define a infraestrutura como código (*Infrastructure as Code*). | https://docs.aws.amazon.com/cdk/ |
| Amazon CloudWatch    | Coleta métricas e *logs* de cada função para observabilidade. | https://docs.aws.amazon.com/cloudwatch/ |
| AWS X-Ray            | Rastreamento distribuído (*tracing*) das requisições entre componentes. | https://docs.aws.amazon.com/xray/ |
| TypeScript           | Linguagem de implementação das funções Lambda. | https://www.typescriptlang.org/docs/ |
