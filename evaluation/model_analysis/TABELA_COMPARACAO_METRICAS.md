# Comparação de Métricas: Benchmark vs Validação

## Resultados da Validação

A validação foi realizada com **10 vídeos** e **296 comentários** que puderam ser pareados entre a API e o dataset histórico (ground truth). Devido à dificuldade de matching entre os comentários retornados pela API do YouTube (ordenados por relevância/tempo) e os comentários históricos do dataset, a amostra é limitada.

### Tabela Comparativa

| Métrica | Benchmark Inicial | Validação Atual | Diferença Absoluta | Diferença Relativa | Status |
|---------|-------------------|-----------------|-------------------|-------------------|--------|
| **Accuracy** | 66.14% | 51.69% | -0.1445 | -21.85% | ⚠ Diferente |
| **Precision** | 66.64% | 68.27% | +0.0163 | +2.45% | ✓ Similar |
| **Recall** | 66.14% | 51.69% | -0.1445 | -21.85% | ⚠ Diferente |
| **F1-Score** | 66.28% | 49.03% | -0.1725 | -26.02% | ⚠ Diferente |

### Interpretação

- **Precision**: Mantém-se similar ao benchmark (+2.45%), indicando que quando o modelo classifica um comentário como uma classe, a confiança nessa classificação se mantém.
- **Accuracy, Recall e F1-Score**: Apresentam diferenças significativas em relação ao benchmark. Isso pode ser devido a:
  1. **Amostra pequena**: Apenas 296 comentários puderam ser pareados (vs 206,445 do benchmark)
  2. **Viés de seleção**: Os comentários que conseguem ser pareados podem não ser representativos
  3. **Diferenças temporais**: Comentários retornados pela API podem ter características diferentes dos históricos

### Limitações da Validação

- **Matching limitado**: A API do YouTube retorna comentários ordenados por relevância/tempo, não necessariamente os mesmos do dataset histórico
- **Amostra reduzida**: Apenas 10 vídeos (de 145 planejados) e 296 comentários (de ~72.500 esperados) puderam ser validados
- **Representatividade**: Os comentários que conseguem ser pareados podem não representar a distribuição completa

### Recomendações

Para uma validação mais robusta das métricas, seria necessário:
1. Usar um conjunto de vídeos com comentários mais estáveis/antigos
2. Implementar matching mais flexível (fuzzy matching, normalização de texto)
3. Considerar validação baseada em distribuições agregadas (como feito no script de validação de distribuição)

---

**Figura:** `metrics_comparison_benchmark_20251122_143447.png` - Gráfico comparativo das métricas

