#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate E2E Test Results Table for Academic Report

This script creates a professional table visualization of the Flutter E2E
integration test results for inclusion in the thesis document.

Author: AI Assistant
Date: November 2, 2025
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np

# Set style for academic publication
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 10

# Test data
test_data = [
    {
        'num': '1',
        'flow': 'Visualizacao de\nlista padrao',
        'functionality': 'Inicializacao do app e\ncarregamento de videos',
        'result': 'PASSOU\n8 videos',
        'time': '~4s'
    },
    {
        'num': '2',
        'flow': 'Busca por\npalavra-chave',
        'functionality': 'Filtro de videos por\ntermo customizado',
        'result': 'PASSOU\n7 videos',
        'time': '~22s'
    },
    {
        'num': '3',
        'flow': 'Ordenacao\npor data',
        'functionality': 'Sort de videos por\npublicacao recente',
        'result': 'PASSOU\nOrdem correta',
        'time': '~23s'
    },
    {
        'num': '4',
        'flow': 'Gerenciamento\nde favoritos',
        'functionality': 'Adicionar e remover\nvideo favorito',
        'result': 'PASSOU\nToggle OK',
        'time': '~13s'
    },
    {
        'num': '5',
        'flow': 'Visualizacao de\ncomentarios',
        'functionality': 'Navegacao e carregamento\nde comentarios',
        'result': 'PASSOU\n100 coment.',
        'time': '~34s'
    },
    {
        'num': '6',
        'flow': 'Filtro sentimento\npositivo',
        'functionality': 'Filtragem por categoria\nde sentimento',
        'result': 'PASSOU\nApenas +',
        'time': '~5s'
    },
    {
        'num': '7',
        'flow': 'Favoritos -\nVideos',
        'functionality': 'Persistencia de video\nfavoritado (Firebase)',
        'result': 'PASSOU\n1 video',
        'time': '~20s'
    },
    {
        'num': '8',
        'flow': 'Favoritos -\nComentarios',
        'functionality': 'Persistencia com retry\ninteligente',
        'result': 'PASSOU\n4 coment.',
        'time': '~20s'
    }
]

# Create figure
fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('tight')
ax.axis('off')

# Column headers (no title - will be added as figure caption in document)
columns = ['#', 'Fluxo Testado', 'Funcionalidade Validada', 'Resultado', 'Tempo']
col_widths = [0.06, 0.22, 0.30, 0.22, 0.10]

# Prepare table data
table_data = []
for test in test_data:
    table_data.append([
        test['num'],
        test['flow'],
        test['functionality'],
        test['result'],
        test['time']
    ])

# Create table
table = ax.table(cellText=table_data,
                colLabels=columns,
                colWidths=col_widths,
                cellLoc='left',
                loc='center',
                bbox=[0.05, 0.05, 0.90, 0.92])

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(9)

# Header styling
for i in range(len(columns)):
    cell = table[(0, i)]
    cell.set_facecolor('#2c3e50')
    cell.set_text_props(weight='bold', color='white', ha='center')
    cell.set_height(0.08)

# Data cells styling
for i in range(1, len(table_data) + 1):
    # Alternate row colors
    row_color = '#ecf0f1' if i % 2 == 0 else 'white'
    
    for j in range(len(columns)):
        cell = table[(i, j)]
        cell.set_facecolor(row_color)
        cell.set_height(0.10)
        
        # Center align for #, Resultado, and Tempo columns
        if j in [0, 3, 4]:
            cell.set_text_props(ha='center')
        
        # Make result column green and bold
        if j == 3:
            cell.set_text_props(weight='bold', color='#27ae60')
        
        # Make # column bold
        if j == 0:
            cell.set_text_props(weight='bold', size=10)

# Add borders
for key, cell in table.get_celld().items():
    cell.set_edgecolor('#95a5a6')
    cell.set_linewidth(0.5)

# Add summary statistics box
summary_text = (
    "Resumo da Execucao:\n"
    "Total de testes: 8\n"
    "Testes aprovados: 8 (100%)\n"
    "Tempo total: 2min 15s (media: 16,9s/teste)\n"
    "Ambiente: Android Emulator (producao)\n"
    "Chamadas API: ~15 requisicoes\n"
    "Interacoes UI: ~40 (taps, texto, navegacao)\n"
    "Operacoes Firebase: leitura/escrita favoritos"
)

# Position summary box
ax.text(0.05, 0.02, summary_text,
        transform=fig.transFigure,
        fontsize=8,
        verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='#e8f5e9', alpha=0.8, edgecolor='#27ae60', linewidth=1.5),
        family='monospace')

# Add legend
legend_text = "Legenda: Todos os testes aprovados com sucesso"
ax.text(0.95, 0.01, legend_text,
        transform=fig.transFigure,
        fontsize=8,
        horizontalalignment='right',
        style='italic',
        color='#7f8c8d')

# Add framework info
framework_text = "Framework: Flutter integration_test + WidgetTester | Binding: IntegrationTestWidgetsFlutterBinding"
ax.text(0.5, 0.00, framework_text,
        transform=fig.transFigure,
        fontsize=7,
        horizontalalignment='center',
        style='italic',
        color='#95a5a6')

# Save figure
timestamp = '20251102'
filename = 'e2e_test_results_table_{}.png'.format(timestamp)
plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print("Tabela gerada com sucesso: {}".format(filename))
print("Resolucao: 300 DPI (qualidade de impressao)")
print("Pronta para insercao no documento Word/DOCX")

plt.close()
