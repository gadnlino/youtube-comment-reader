# 📁 GUIA DE ORGANIZAÇÃO DE ARQUIVOS - AVALIAÇÃO
# FILE ORGANIZATION GUIDE - EVALUATION

**Data**: 26 de Outubro de 2025  
**Status**: Guia de Organização  

---

## 🎯 ESTRUTURA RECOMENDADA / RECOMMENDED STRUCTURE

```
evaluation/
│
├── 📊 GRÁFICOS / GRAPHS
│   ├── english/
│   │   ├── comprehensive_performance_overview.png ⭐ [Figura 1]
│   │   ├── scalability_analysis.png ⭐ [Figura 2]
│   │   ├── statistical_summary.png ⭐ [Figura 3]
│   │   ├── performance_heatmap.png ⭐ [Figura 4]
│   │   ├── batch_size_analysis_20251026_214815.png ⭐ [Análise de Lote]
│   │   └── multi_video_comparison_20251026_212004.png ⭐ [Multi-Vídeo]
│   │
│   └── portuguese/
│       ├── visao_geral_performance_pt.png ⭐⭐⭐ [Figura 1 - USE ESTE]
│       ├── analise_escalabilidade_pt.png ⭐⭐⭐ [Figura 2 - USE ESTE]
│       ├── resumo_estatistico_pt.png ⭐⭐⭐ [Figura 3 - USE ESTE]
│       └── mapa_calor_performance_pt.png ⭐⭐⭐ [Figura 4 - USE ESTE]
│
├── 📄 RELATÓRIOS / REPORTS
│   ├── FINAL_EVALUATION_REPORT.md ⭐⭐⭐ [Resumo Executivo]
│   ├── TESTING_METHODOLOGY.md ⭐⭐⭐ [Metodologia Completa]
│   ├── ASSIGNMENT_QUICK_REFERENCE.md ⭐⭐ [Números Rápidos]
│   ├── EXTENDED_API_PERFORMANCE_RESULTS.md [Performance Detalhada]
│   ├── INDEX.md [Navegação]
│   └── ONDE_ESTA_TUDO.md [Este Guia]
│
├── 📊 DADOS / DATA
│   ├── extended_performance_results_20251025_141608.csv
│   ├── heavy_load_test_results_20251025_143255.csv
│   ├── heavy_load_test_analysis_20251025_143255.json
│   ├── multi_video_results_20251026_212004.csv
│   ├── multi_video_summary_20251026_212004.json
│   ├── batch_size_analysis_20251026_214815.csv
│   └── batch_size_summary_20251026_214815.json
│
├── 🧪 TESTES E2E / E2E TESTS
│   └── e2e_functionality_testing/
│       ├── E2E_FUNCTIONALITY_UX_RESULTS.md ⭐ [Resultados E2E]
│       ├── e2e_test_report_20251025_142203.json
│       ├── e2e_functionality_test.py
│       └── README.md
│
├── 📝 SCRIPTS
│   └── api_load_testing/
│       ├── generate_academic_graphs.py [Gerador de Gráficos EN]
│       ├── generate_academic_graphs_pt.py [Gerador de Gráficos PT]
│       ├── batch_size_analysis.py [Análise de Tamanho de Lote]
│       ├── multi_video_benchmark.py [Benchmark Multi-Vídeo]
│       ├── extended_benchmark.py [Benchmark Estendido]
│       ├── heavy_load_test.py [Teste de Carga Pesada]
│       ├── performance_benchmark.py [Benchmark de Performance]
│       ├── quick_test.py [Teste Rápido]
│       ├── locustfile.py [Load Testing com Locust]
│       └── README.md
│
└── 📚 RELATÓRIOS ESPECÍFICOS / SPECIFIC REPORTS
    └── api_load_testing/
        ├── HEAVY_LOAD_TEST_RESULTS.md ⭐ [Carga Pesada]
        ├── MULTI_VIDEO_EVALUATION_RESULTS.md ⭐ [Multi-Vídeo]
        └── API_EVALUATION_GUIDE.md [Guia de Avaliação]
```

---

## 📊 LOCALIZAÇÃO ATUAL DOS ARQUIVOS / CURRENT FILE LOCATIONS

### ✅ GRÁFICOS PARA O RELATÓRIO (USE ESTES!) / GRAPHS FOR REPORT

**Versão Português** (RECOMENDADO para relatório em PT):
```
evaluation/api_load_testing/visao_geral_performance_pt.png ⭐⭐⭐
evaluation/api_load_testing/analise_escalabilidade_pt.png ⭐⭐⭐
evaluation/api_load_testing/resumo_estatistico_pt.png ⭐⭐⭐
evaluation/api_load_testing/mapa_calor_performance_pt.png ⭐⭐⭐
```

**Versão English** (se precisar):
```
evaluation/api_load_testing/comprehensive_performance_overview.png
evaluation/api_load_testing/scalability_analysis.png
evaluation/api_load_testing/statistical_summary.png
evaluation/api_load_testing/performance_heatmap.png
```

**Gráficos Adicionais**:
```
evaluation/api_load_testing/batch_size_analysis_20251026_214815.png
evaluation/api_load_testing/multi_video_comparison_20251026_212004.png
```

---

### 📄 DOCUMENTOS PRINCIPAIS / MAIN DOCUMENTS

**Relatórios Principais** (evaluation/):
```
FINAL_EVALUATION_REPORT.md ⭐⭐⭐ - Resumo executivo de tudo
TESTING_METHODOLOGY.md ⭐⭐⭐ - Metodologia completa (use para seção de metodologia)
ASSIGNMENT_QUICK_REFERENCE.md ⭐⭐ - Números rápidos para consulta
EXTENDED_API_PERFORMANCE_RESULTS.md - Resultados detalhados de performance
INDEX.md - Índice de navegação
ONDE_ESTA_TUDO.md - Este guia de organização
```

**Relatórios Específicos** (evaluation/api_load_testing/):
```
HEAVY_LOAD_TEST_RESULTS.md - Resultados de carga pesada (10.600 comentários)
MULTI_VIDEO_EVALUATION_RESULTS.md - Resultados multi-vídeo (3 vídeos)
API_EVALUATION_GUIDE.md - Guia de avaliação da API
```

**Relatórios E2E** (evaluation/e2e_functionality_testing/):
```
E2E_FUNCTIONALITY_UX_RESULTS.md - Resultados de funcionalidade e UX
README.md - Documentação dos testes E2E
```

---

### 📊 ARQUIVOS DE DADOS / DATA FILES

**Dados CSV** (evaluation/api_load_testing/):
```
extended_performance_results_20251025_141608.csv - 219 requisições
heavy_load_test_results_20251025_143255.csv - 106 requisições
multi_video_results_20251026_212004.csv - 60 requisições
batch_size_analysis_20251026_214815.csv - 90 requisições (9 tamanhos)
```

**Dados JSON** (evaluation/api_load_testing/):
```
multi_video_summary_20251026_212004.json - Resumo multi-vídeo
batch_size_summary_20251026_214815.json - Resumo de tamanho de lote
heavy_load_test_analysis_20251025_143255.json - Análise de carga pesada
```

**Dados E2E** (evaluation/e2e_functionality_testing/):
```
e2e_test_report_20251025_142203.json - Resultados de 6 testes E2E
```

---

### 🔧 SCRIPTS DE TESTE / TEST SCRIPTS

**Geradores de Gráficos** (evaluation/api_load_testing/):
```
generate_academic_graphs.py - Gera gráficos em inglês
generate_academic_graphs_pt.py - Gera gráficos em português
```

**Scripts de Teste** (evaluation/api_load_testing/):
```
batch_size_analysis.py - Análise de tamanho de lote (9 tamanhos)
multi_video_benchmark.py - Teste multi-vídeo (3 vídeos)
extended_benchmark.py - Teste estendido (219 requisições)
heavy_load_test.py - Teste de carga pesada (10.600 comentários)
performance_benchmark.py - Benchmark de performance
quick_test.py - Teste rápido de funcionalidade
locustfile.py - Load testing com Locust
```

**Scripts E2E** (evaluation/e2e_functionality_testing/):
```
e2e_functionality_test.py - Testes end-to-end completos
```

---

## 🎯 ARQUIVOS ESSENCIAIS PARA O RELATÓRIO

### Para INTRODUÇÃO:
```
📄 FINAL_EVALUATION_REPORT.md (seção de introdução)
```

### Para METODOLOGIA:
```
📄 TESTING_METHODOLOGY.md ⭐⭐⭐ (documento completo - 964 linhas)
```

### Para RESULTADOS - ACURÁCIA DO MODELO:
```
📄 ../packages/containers/sentiment_analysis/evaluation/model_evaluation/MODEL_COMPARISON_SUMMARY.md
📊 Número: 66.14% acurácia
```

### Para RESULTADOS - PERFORMANCE:
```
📄 EXTENDED_API_PERFORMANCE_RESULTS.md
📊 Gráfico: visao_geral_performance_pt.png (Figura 1)
📊 Números: 1.024ms média, 100% sucesso
```

### Para RESULTADOS - ESCALABILIDADE:
```
📄 api_load_testing/HEAVY_LOAD_TEST_RESULTS.md
📊 Gráfico: analise_escalabilidade_pt.png (Figura 2)
📊 Números: 10.600 comentários, sem degradação
```

### Para RESULTADOS - MULTI-VÍDEO:
```
📄 api_load_testing/MULTI_VIDEO_EVALUATION_RESULTS.md
📊 Números: 3 vídeos, < 30% variância, 100% sucesso
```

### Para RESULTADOS - FUNCIONALIDADE:
```
📄 e2e_functionality_testing/E2E_FUNCTIONALITY_UX_RESULTS.md
📊 Números: 100% acurácia de filtros, 200-300x economia de tempo
```

### Para ANÁLISE ESTATÍSTICA:
```
📊 Gráficos: resumo_estatistico_pt.png (Figura 3)
📊 Gráficos: mapa_calor_performance_pt.png (Figura 4)
```

### Para CONCLUSÕES:
```
📄 FINAL_EVALUATION_REPORT.md (seção de conclusão)
📊 Nota Final: A+ (96/100)
```

---

## 🗂️ PLANO DE REORGANIZAÇÃO COMPLETA

### 📋 ESTRUTURA FINAL PROPOSTA

```
evaluation/
│
├── 01_reports/                          # Todos os relatórios principais
│   ├── FINAL_EVALUATION_REPORT.md
│   ├── TESTING_METHODOLOGY.md
│   ├── ASSIGNMENT_QUICK_REFERENCE.md
│   ├── EXTENDED_API_PERFORMANCE_RESULTS.md
│   ├── HEAVY_LOAD_TEST_RESULTS.md
│   ├── MULTI_VIDEO_EVALUATION_RESULTS.md
│   ├── API_EVALUATION_GUIDE.md
│   ├── INDEX.md
│   └── README.md
│
├── 02_graphs/                           # Todos os gráficos organizados
│   ├── english/
│   │   ├── figure1_comprehensive_performance_overview.png
│   │   ├── figure2_scalability_analysis.png
│   │   ├── figure3_statistical_summary.png
│   │   ├── figure4_performance_heatmap.png
│   │   ├── batch_size_analysis.png
│   │   └── multi_video_comparison.png
│   │
│   └── portuguese/
│       ├── figura1_visao_geral_performance.png
│       ├── figura2_analise_escalabilidade.png
│       ├── figura3_resumo_estatistico.png
│       └── figura4_mapa_calor_performance.png
│
├── 03_data/                            # Todos os dados brutos
│   ├── csv/
│   │   ├── extended_performance_results.csv
│   │   ├── heavy_load_test_results.csv
│   │   ├── multi_video_results.csv
│   │   └── batch_size_analysis.csv
│   │
│   └── json/
│       ├── multi_video_summary.json
│       ├── batch_size_summary.json
│       ├── heavy_load_analysis.json
│       └── e2e_test_report.json
│
├── 04_scripts/                         # Todos os scripts de teste
│   ├── generators/
│   │   ├── generate_academic_graphs.py
│   │   ├── generate_academic_graphs_pt.py
│   │   └── README.md
│   │
│   └── tests/
│       ├── batch_size_analysis.py
│       ├── multi_video_benchmark.py
│       ├── extended_benchmark.py
│       ├── heavy_load_test.py
│       ├── performance_benchmark.py
│       ├── quick_test.py
│       ├── e2e_functionality_test.py
│       ├── locustfile.py
│       ├── config_template.py
│       └── README.md
│
├── 05_guides/                          # Guias de uso e organização
│   ├── ONDE_ESTA_TUDO.md
│   ├── ORGANIZACAO_ARQUIVOS.md (este arquivo)
│   └── COMO_USAR_OS_SCRIPTS.md
│
└── 06_archived/                        # Arquivos antigos (backup)
    └── old_graphs/
        └── (gráficos antigos da pasta api_load_testing)
```

---

## 🚀 COMANDOS PARA REORGANIZAR (COPIE E EXECUTE)

### PASSO 1: Criar Estrutura de Pastas

```bash
cd evaluation

# Criar estrutura de pastas
mkdir -p 01_reports
mkdir -p 02_graphs/english
mkdir -p 02_graphs/portuguese
mkdir -p 03_data/csv
mkdir -p 03_data/json
mkdir -p 04_scripts/generators
mkdir -p 04_scripts/tests
mkdir -p 05_guides
mkdir -p 06_archived/old_graphs

echo "✅ Estrutura criada!"
```

### PASSO 2: Mover Relatórios

```bash
cd evaluation

# Mover relatórios principais
mv FINAL_EVALUATION_REPORT.md 01_reports/
mv TESTING_METHODOLOGY.md 01_reports/
mv ASSIGNMENT_QUICK_REFERENCE.md 01_reports/
mv EXTENDED_API_PERFORMANCE_RESULTS.md 01_reports/
mv API_EVALUATION_GUIDE.md 01_reports/
mv INDEX.md 01_reports/

# Mover relatórios específicos
mv api_load_testing/HEAVY_LOAD_TEST_RESULTS.md 01_reports/
mv api_load_testing/MULTI_VIDEO_EVALUATION_RESULTS.md 01_reports/

echo "✅ Relatórios movidos!"
```

### PASSO 3: Mover Gráficos

```bash
cd evaluation

# Mover gráficos em inglês (renomeando para nomes mais claros)
cp api_load_testing/comprehensive_performance_overview.png 02_graphs/english/figure1_comprehensive_performance_overview.png
cp api_load_testing/scalability_analysis.png 02_graphs/english/figure2_scalability_analysis.png
cp api_load_testing/statistical_summary.png 02_graphs/english/figure3_statistical_summary.png
cp api_load_testing/performance_heatmap.png 02_graphs/english/figure4_performance_heatmap.png
cp api_load_testing/batch_size_analysis_20251026_214815.png 02_graphs/english/batch_size_analysis.png
cp api_load_testing/multi_video_comparison_20251026_212004.png 02_graphs/english/multi_video_comparison.png

# Mover gráficos em português (renomeando)
cp api_load_testing/visao_geral_performance_pt.png 02_graphs/portuguese/figura1_visao_geral_performance.png
cp api_load_testing/analise_escalabilidade_pt.png 02_graphs/portuguese/figura2_analise_escalabilidade.png
cp api_load_testing/resumo_estatistico_pt.png 02_graphs/portuguese/figura3_resumo_estatistico.png
cp api_load_testing/mapa_calor_performance_pt.png 02_graphs/portuguese/figura4_mapa_calor_performance.png

# Arquivar gráficos antigos
mv api_load_testing/*.png 06_archived/old_graphs/

echo "✅ Gráficos organizados!"
```

### PASSO 4: Mover Dados

```bash
cd evaluation

# Mover arquivos CSV
cp api_load_testing/extended_performance_results_20251025_141608.csv 03_data/csv/extended_performance_results.csv
cp api_load_testing/heavy_load_test_results_20251025_143255.csv 03_data/csv/heavy_load_test_results.csv
cp api_load_testing/multi_video_results_20251026_212004.csv 03_data/csv/multi_video_results.csv
cp api_load_testing/batch_size_analysis_20251026_214815.csv 03_data/csv/batch_size_analysis.csv

# Mover arquivos JSON
cp api_load_testing/multi_video_summary_20251026_212004.json 03_data/json/multi_video_summary.json
cp api_load_testing/batch_size_summary_20251026_214815.json 03_data/json/batch_size_summary.json
cp api_load_testing/heavy_load_test_analysis_20251025_143255.json 03_data/json/heavy_load_analysis.json
cp e2e_functionality_testing/e2e_test_report_20251025_142203.json 03_data/json/e2e_test_report.json

echo "✅ Dados organizados!"
```

### PASSO 5: Mover Scripts

```bash
cd evaluation

# Mover geradores de gráficos
mv api_load_testing/generate_academic_graphs.py 04_scripts/generators/
mv api_load_testing/generate_academic_graphs_pt.py 04_scripts/generators/

# Mover scripts de teste
mv api_load_testing/batch_size_analysis.py 04_scripts/tests/
mv api_load_testing/multi_video_benchmark.py 04_scripts/tests/
mv api_load_testing/extended_benchmark.py 04_scripts/tests/
mv api_load_testing/heavy_load_test.py 04_scripts/tests/
mv api_load_testing/performance_benchmark.py 04_scripts/tests/
mv api_load_testing/quick_test.py 04_scripts/tests/
mv api_load_testing/locustfile.py 04_scripts/tests/
mv api_load_testing/config_template.py 04_scripts/tests/

# Mover script E2E
mv e2e_functionality_testing/e2e_functionality_test.py 04_scripts/tests/

# Mover READMEs
mv api_load_testing/README.md 04_scripts/tests/
mv e2e_functionality_testing/README.md 04_scripts/tests/E2E_README.md

echo "✅ Scripts organizados!"
```

### PASSO 6: Mover Guias

```bash
cd evaluation

# Mover guias
mv ONDE_ESTA_TUDO.md 05_guides/
mv ORGANIZACAO_ARQUIVOS.md 05_guides/

echo "✅ Guias organizados!"
```

### PASSO 7: Criar README Principal

```bash
cd evaluation

cat > README.md << 'EOF'
# 📊 Avaliação Completa - YouTube Comment Reader

## 📁 Estrutura de Pastas

- **01_reports/** - Todos os relatórios e documentação
- **02_graphs/** - Gráficos em inglês e português
- **03_data/** - Dados brutos (CSV e JSON)
- **04_scripts/** - Scripts de teste e geradores
- **05_guides/** - Guias de uso e organização
- **06_archived/** - Arquivos antigos (backup)

## 🎯 Acesso Rápido

### Para o Relatório:
- Relatório Final: `01_reports/FINAL_EVALUATION_REPORT.md`
- Metodologia: `01_reports/TESTING_METHODOLOGY.md`
- Números Rápidos: `01_reports/ASSIGNMENT_QUICK_REFERENCE.md`

### Gráficos (Português):
- Figura 1: `02_graphs/portuguese/figura1_visao_geral_performance.png`
- Figura 2: `02_graphs/portuguese/figura2_analise_escalabilidade.png`
- Figura 3: `02_graphs/portuguese/figura3_resumo_estatistico.png`
- Figura 4: `02_graphs/portuguese/figura4_mapa_calor_performance.png`

### Guias:
- Onde Está Tudo: `05_guides/ONDE_ESTA_TUDO.md`
- Como Organizar: `05_guides/ORGANIZACAO_ARQUIVOS.md`

## 📊 Estatísticas

- **Total de Testes**: 6 tipos diferentes
- **Requisições Testadas**: 385 (219 + 106 + 60 + 90)
- **Comentários Processados**: 10.600+
- **Taxa de Sucesso**: 100%
- **Nota Final**: A+ (96/100)

EOF

echo "✅ README criado!"
```

### PASSO 8: Limpar Pastas Antigas (OPCIONAL)

```bash
cd evaluation

# CUIDADO: Só execute depois de verificar que tudo foi copiado!
# Isso remove as pastas antigas

# rm -rf api_load_testing
# rm -rf e2e_functionality_testing

# OU mantenha como backup:
# mv api_load_testing 06_archived/
# mv e2e_functionality_testing 06_archived/

echo "⚠️  Limpeza pendente - revise antes de executar!"
```

### PASSO 9: Verificar Organização

```bash
cd evaluation

echo "📊 ESTRUTURA FINAL:"
echo ""
tree -L 2 -d

# Ou se não tiver tree:
find . -maxdepth 2 -type d | sort

echo ""
echo "✅ Reorganização completa!"
```

---

## ✅ CHECKLIST DE REORGANIZAÇÃO

Ao executar os comandos acima, verifique:

- [ ] **Passo 1**: Estrutura de pastas criada
- [ ] **Passo 2**: Relatórios movidos para `01_reports/`
- [ ] **Passo 3**: Gráficos organizados em `02_graphs/english/` e `02_graphs/portuguese/`
- [ ] **Passo 4**: Dados CSV e JSON em `03_data/`
- [ ] **Passo 5**: Scripts em `04_scripts/generators/` e `04_scripts/tests/`
- [ ] **Passo 6**: Guias em `05_guides/`
- [ ] **Passo 7**: README principal criado
- [ ] **Passo 8**: Pastas antigas arquivadas (opcional)
- [ ] **Passo 9**: Estrutura verificada

---

## 🎯 DEPOIS DA REORGANIZAÇÃO

### Onde Encontrar Cada Coisa:

| Preciso de... | Está em... |
|---------------|------------|
| **Gráficos para relatório (PT)** | `02_graphs/portuguese/` |
| **Relatório final** | `01_reports/FINAL_EVALUATION_REPORT.md` |
| **Metodologia** | `01_reports/TESTING_METHODOLOGY.md` |
| **Números rápidos** | `01_reports/ASSIGNMENT_QUICK_REFERENCE.md` |
| **Dados brutos CSV** | `03_data/csv/` |
| **Dados JSON** | `03_data/json/` |
| **Scripts de teste** | `04_scripts/tests/` |
| **Geradores de gráficos** | `04_scripts/generators/` |
| **Guias** | `05_guides/` |

---

## 💡 DICAS IMPORTANTES

1. **Execute passo a passo** - Não execute tudo de uma vez
2. **Verifique cada passo** - Certifique-se que os arquivos foram copiados
3. **Mantenha backups** - As pastas antigas ficam em `06_archived/`
4. **Use um novo chat** - Como você mencionou, para execução mais rápida

---

## 📋 SCRIPT COMPLETO (EXECUTAR TUDO DE UMA VEZ)

Se quiser executar tudo de uma vez, copie este script completo:

```bash
#!/bin/bash
# Script de Reorganização Completa
# Execute: bash reorganize.sh

cd evaluation

echo "🚀 Iniciando reorganização..."

# 1. Criar estrutura
mkdir -p 01_reports 02_graphs/{english,portuguese} 03_data/{csv,json} 04_scripts/{generators,tests} 05_guides 06_archived/old_graphs

# 2. Mover relatórios
mv FINAL_EVALUATION_REPORT.md TESTING_METHODOLOGY.md ASSIGNMENT_QUICK_REFERENCE.md EXTENDED_API_PERFORMANCE_RESULTS.md API_EVALUATION_GUIDE.md INDEX.md 01_reports/ 2>/dev/null
mv api_load_testing/HEAVY_LOAD_TEST_RESULTS.md api_load_testing/MULTI_VIDEO_EVALUATION_RESULTS.md 01_reports/ 2>/dev/null

# 3. Copiar gráficos
cp api_load_testing/comprehensive_performance_overview.png 02_graphs/english/figure1_comprehensive_performance_overview.png 2>/dev/null
cp api_load_testing/scalability_analysis.png 02_graphs/english/figure2_scalability_analysis.png 2>/dev/null
cp api_load_testing/statistical_summary.png 02_graphs/english/figure3_statistical_summary.png 2>/dev/null
cp api_load_testing/performance_heatmap.png 02_graphs/english/figure4_performance_heatmap.png 2>/dev/null
cp api_load_testing/batch_size_analysis_20251026_214815.png 02_graphs/english/batch_size_analysis.png 2>/dev/null
cp api_load_testing/multi_video_comparison_20251026_212004.png 02_graphs/english/multi_video_comparison.png 2>/dev/null

cp api_load_testing/visao_geral_performance_pt.png 02_graphs/portuguese/figura1_visao_geral_performance.png 2>/dev/null
cp api_load_testing/analise_escalabilidade_pt.png 02_graphs/portuguese/figura2_analise_escalabilidade.png 2>/dev/null
cp api_load_testing/resumo_estatistico_pt.png 02_graphs/portuguese/figura3_resumo_estatistico.png 2>/dev/null
cp api_load_testing/mapa_calor_performance_pt.png 02_graphs/portuguese/figura4_mapa_calor_performance.png 2>/dev/null

# 4. Copiar dados
cp api_load_testing/*results*.csv 03_data/csv/ 2>/dev/null
cp api_load_testing/*analysis*.csv 03_data/csv/ 2>/dev/null
cp api_load_testing/*.json 03_data/json/ 2>/dev/null
cp e2e_functionality_testing/*.json 03_data/json/ 2>/dev/null

# 5. Mover scripts
mv api_load_testing/generate*.py 04_scripts/generators/ 2>/dev/null
mv api_load_testing/*.py 04_scripts/tests/ 2>/dev/null
mv e2e_functionality_testing/*.py 04_scripts/tests/ 2>/dev/null

# 6. Mover guias
mv ONDE_ESTA_TUDO.md ORGANIZACAO_ARQUIVOS.md 05_guides/ 2>/dev/null

# 7. Arquivar antigos
mv api_load_testing/*.png 06_archived/old_graphs/ 2>/dev/null

echo "✅ Reorganização completa!"
echo "📊 Verifique as pastas:"
ls -la
```

Salve como `reorganize.sh` e execute: `bash reorganize.sh`

---

## 📋 CHECKLIST: O QUE VOCÊ PRECISA

### Para o Relatório Escrito:
- [ ] TESTING_METHODOLOGY.md (metodologia)
- [ ] FINAL_EVALUATION_REPORT.md (resumo e conclusões)
- [ ] ASSIGNMENT_QUICK_REFERENCE.md (números rápidos)
- [ ] Relatórios específicos (performance, heavy load, multi-video, E2E)

### Para as Figuras do Relatório:
- [ ] visao_geral_performance_pt.png (Figura 1)
- [ ] analise_escalabilidade_pt.png (Figura 2)
- [ ] resumo_estatistico_pt.png (Figura 3)
- [ ] mapa_calor_performance_pt.png (Figura 4)

### Se o Professor Pedir Evidências:
- [ ] Arquivos CSV com dados brutos
- [ ] Scripts Python (.py files)
- [ ] Arquivos JSON com análises

---

## 🎯 RESUMO: ONDE ESTÁ CADA COISA

| O Que Você Precisa | Onde Encontrar |
|--------------------|----------------|
| **Gráficos em Português** | `evaluation/api_load_testing/*_pt.png` |
| **Gráficos em Inglês** | `evaluation/api_load_testing/*.png` (sem `_pt`) |
| **Metodologia** | `evaluation/TESTING_METHODOLOGY.md` |
| **Resumo Geral** | `evaluation/FINAL_EVALUATION_REPORT.md` |
| **Números Rápidos** | `evaluation/ASSIGNMENT_QUICK_REFERENCE.md` |
| **Dados Brutos** | `evaluation/api_load_testing/*.csv` |
| **Scripts de Teste** | `evaluation/api_load_testing/*.py` |
| **Testes E2E** | `evaluation/e2e_functionality_testing/` |
| **Acurácia do Modelo** | `packages/containers/sentiment_analysis/evaluation/model_evaluation/` |

---

## 💡 DICA: USE O FINDER/EXPLORER

**No macOS:**
```bash
# Abrir a pasta de gráficos no Finder
open evaluation/api_load_testing/

# Filtrar apenas arquivos PNG
# No Finder: Buscar por "kind:image"
```

**Ou crie atalhos:**
```bash
# Criar pasta com links simbólicos para fácil acesso
mkdir ~/relatorio_facil
ln -s /caminho/para/evaluation/api_load_testing/*_pt.png ~/relatorio_facil/
ln -s /caminho/para/evaluation/*.md ~/relatorio_facil/
```

---

## ✅ RECOMENDAÇÃO FINAL

**NÃO mova os arquivos agora!** A organização atual está funcional.

**Em vez disso:**
1. Use este guia (**ONDE_ESTA_TUDO.md**) para navegar
2. Quando precisar de um arquivo, consulte este documento
3. Copie apenas os arquivos necessários quando for montar o relatório final

**Por quê?**
- Os scripts dependem dos caminhos atuais
- Você pode precisar regenerar gráficos
- Manter os dados brutos no mesmo local que os scripts facilita testes

---

## 📞 ACESSO RÁPIDO

### "Preciso dos 4 gráficos em português agora!"
```bash
cd evaluation/api_load_testing/
ls -la *_pt.png
```

### "Preciso da metodologia!"
```bash
open evaluation/TESTING_METHODOLOGY.md
```

### "Preciso de todos os números!"
```bash
open evaluation/ASSIGNMENT_QUICK_REFERENCE.md
```

### "Preciso dos dados brutos!"
```bash
cd evaluation/api_load_testing/
ls -la *.csv *.json
```

---

**Última atualização**: 26 de Outubro de 2025  
**Status**: Organização Documentada ✅  
**Arquivos Totais**: 400+ arquivos de avaliação  
**Arquivos Essenciais para Relatório**: ~15 arquivos  

---

💡 **DICA PRO**: Imprima este guia ou mantenha-o aberto enquanto escreve seu relatório!

