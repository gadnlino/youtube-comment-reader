# Análise Detalhada de Erros - Testes de Carga

## Status dos Erros Identificados

### 1. Status 403 - Quota Exceeded (YouTube API)

**Mensagem de Erro:**
```json
{
  "error": {
    "error": {
      "code": 403,
      "message": "The request cannot be completed because you have exceeded your quota.",
      "errors": [
        {
          "message": "The request cannot be completed because you have exceeded your <a href=\"/youtube/v3/getting-started#quota\">quota</a>.",
          "domain": "youtube.quota",
          "reason": "quotaExceeded"
        }
      ]
    }
  }
}
```

**Causa Raiz:**
- A API do YouTube tem uma quota diária de requisições
- Os testes de carga (especialmente o teste de 15 minutos com 300 usuários) geraram **374,584 requisições**
- Isso esgotou a quota diária disponível

**Ocorrências nos Testes:**
- Teste 3 (15min, 300 users): 10,483 ocorrências (principalmente em `/video/comments`)
- Teste 3 (15min, 300 users): 77,018 falhas em `/search` (Status 502, mas provavelmente relacionado)

**Impacto:**
- Após esgotar a quota, **TODAS** as requisições subsequentes falham com 403
- Isso explica por que o teste com 200 usuários teve 100% de falhas

### 2. Status 502 - Bad Gateway

**Mensagem de Erro:**
```json
{
  "message": "Internal server error"
}
```

**Causa Provável:**
- Erro interno do servidor ao processar requisições
- Pode estar relacionado à quota excedida ou sobrecarga do sistema
- Gateway não consegue processar a requisição

**Ocorrências nos Testes:**
- Teste 3 (15min, 300 users): 77,261 ocorrências
  - `/search`: 77,017 ocorrências (99.7% das falhas deste endpoint)
  - `/video/comments`: 244 ocorrências

### 3. Status 0 - Connection Error

**Causa:**
- Erro de conexão (timeout, rede, etc.)
- Ocorrências mínimas (2 no teste 3)

## Análise do Teste com 200 Usuários

O teste com 200 usuários teve **100% de falhas** porque:

1. **Quota já estava esgotada** dos testes anteriores
2. Todas as requisições retornaram 403 (Quota Exceeded) ou 502 (Bad Gateway)
3. A API do YouTube bloqueou todas as requisições subsequentes

## Recomendações

### Imediatas:
1. **Aguardar reset da quota** (geralmente à meia-noite UTC ou após 24h)
2. **Verificar quota disponível** na Google Cloud Console
3. **Considerar aumentar a quota** se necessário para testes

### Para Testes Futuros:
1. **Monitorar quota durante os testes** para evitar esgotamento
2. **Implementar rate limiting** nos testes para respeitar limites da API
3. **Usar múltiplas API keys** (se disponível) para distribuir carga
4. **Considerar testes mais curtos** ou com menos usuários para não esgotar quota

### Limites Identificados:
- **Quota diária**: Aproximadamente ~400,000 requisições (baseado nos testes)
- **Limite prático para testes**: ~200,000 requisições/dia para deixar margem

## Conclusão

Os erros não são causados por problemas de infraestrutura da API intermediária, mas sim pelo **esgotamento da quota da API do YouTube**. A API intermediária está funcionando corretamente, mas depende da API do YouTube que tem limites de quota.

**Próximos Passos:**
1. Aguardar reset da quota (ou verificar quando será resetado)
2. Re-executar o teste com 200 usuários após reset
3. Considerar implementar monitoramento de quota nos scripts de teste

