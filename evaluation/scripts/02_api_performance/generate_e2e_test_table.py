#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera tabela visual dos resultados dos testes E2E do Flutter (Tabela 4 da monografia).

Cria uma tabela formatada com:
- Número do teste
- Fluxo testado
- Funcionalidade validada (com descrição detalhada)
- Resultado
- Tempo de execução

Uso (a partir da raiz do repositório):

    # Cópia com timestamp em evaluation/api_load_testing/graphs/
    python3 evaluation/scripts/02_api_performance/generate_e2e_test_table.py

    # Regenera também o PNG canônico da monografia (Tabela 4)
    python3 evaluation/scripts/02_api_performance/generate_e2e_test_table.py --thesis

Os dados embutidos em TESTES refletem a execução documentada na monografia.
Para atualizar a tabela, edite TESTES (e o resumo em generate_e2e_test_table)
e execute novamente com --thesis.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _paths import API_GRAPHS, GRAPHS

# Dados dos testes baseados nos testes críticos do Flutter
TESTES = [
    {
        'numero': 1,
        'fluxo': 'Visualização de lista padrão',
        'funcionalidade': 'Inicialização do app e carregamento de vídeos da API do YouTube',
        'resultado': 'PASSOU 8 vídeos',
        'tempo': '~4s'
    },
    {
        'numero': 2,
        'fluxo': 'Busca por palavra-chave',
        'funcionalidade': 'Filtro de vídeos por termo customizado via modal de busca',
        'resultado': 'PASSOU 7 vídeos',
        'tempo': '~22s'
    },
    {
        'numero': 3,
        'fluxo': 'Ordenação por data',
        'funcionalidade': 'Sort de vídeos por data de publicação (mais recentes primeiro)',
        'resultado': 'PASSOU Ordem correta',
        'tempo': '~23s'
    },
    {
        'numero': 4,
        'fluxo': 'Gerenciamento de favoritos',
        'funcionalidade': 'Toggle de favoritar/desfavoritar vídeo com mudança visual do ícone',
        'resultado': 'PASSOU Toggle OK',
        'tempo': '~13s'
    },
    {
        'numero': 5,
        'fluxo': 'Visualização de comentários',
        'funcionalidade': 'Navegação para página de comentários e carregamento assíncrono via API',
        'resultado': 'PASSOU 100 coment.',
        'tempo': '~34s'
    },
    {
        'numero': 6,
        'fluxo': 'Filtro sentimento positivo',
        'funcionalidade': 'Filtragem de comentários por sentimento positivo com validação de 100% de acurácia',
        'resultado': 'PASSOU Apenas +',
        'tempo': '~5s'
    },
    {
        'numero': 7,
        'fluxo': 'Favoritos - Vídeos',
        'funcionalidade': 'Persistência local de vídeo favoritado no dispositivo e exibição na aba Favorites',
        'resultado': 'PASSOU 1 vídeo',
        'tempo': '~20s'
    },
    {
        'numero': 8,
        'fluxo': 'Favoritos - Comentários',
        'funcionalidade': 'Persistência local de comentário favoritado no dispositivo com retry em caso de falha',
        'resultado': 'PASSOU 4 coment.',
        'tempo': '~20s'
    }
]

# Nome canônico do PNG embutido na monografia (Tabela 4)
THESIS_TABLE_4 = GRAPHS / "tables" / "tabela-4_e2e_test_results_table.png"


def generate_e2e_test_table(thesis: bool = False) -> list[Path]:
    """Gera tabela visual dos testes E2E. Retorna os caminhos dos arquivos gravados."""

    # Criar figura para acomodar tabela
    fig = plt.figure(figsize=(22, 10))
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Preparar dados da tabela
    table_data = []
    headers = ['#', 'Fluxo Testado', 'Funcionalidade Validada', 'Resultado', 'Tempo']

    for teste in TESTES:
        table_data.append([
            str(teste['numero']),
            teste['fluxo'],
            teste['funcionalidade'],
            teste['resultado'],
            teste['tempo']
        ])

    # Criar tabela
    table = ax.table(
        cellText=table_data,
        colLabels=headers,
        cellLoc='left',
        loc='center',
        colWidths=[0.03, 0.18, 0.55, 0.14, 0.10]
    )

    # Ajustar fonte e altura das células
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.8)

    # Colorir células de resultado (verde para PASSOU)
    for i in range(len(table_data)):
        # Coluna de resultado
        table[(i+1, 3)].set_facecolor('#d4edda')  # Verde claro
        table[(i+1, 3)].set_text_props(weight='bold', fontsize=10)

        # Coluna de número
        table[(i+1, 0)].set_facecolor('#e9ecef')  # Cinza claro
        table[(i+1, 0)].set_text_props(weight='bold', fontsize=11)

    # Estilizar cabeçalho
    for j in range(len(headers)):
        table[(0, j)].set_facecolor('#343a40')  # Cinza escuro
        table[(0, j)].set_text_props(weight='bold', color='white', fontsize=13)
        table[(0, j)].set_height(0.10)

    # Ajustar fonte das colunas
    for i in range(len(table_data)):
        table[(i+1, 0)].set_text_props(fontsize=12, weight='bold')
        table[(i+1, 1)].set_text_props(fontsize=11, weight='bold')
        table[(i+1, 2)].set_text_props(fontsize=10.5)
        table[(i+1, 3)].set_text_props(fontsize=11, weight='bold')
        table[(i+1, 4)].set_text_props(fontsize=11)

    # Título
    ax.set_title('Resultados dos Testes End-to-End - Aplicação Flutter',
                 fontsize=16, fontweight='bold', pad=20)

    # Resumo da execução
    total_testes = len(TESTES)
    testes_aprovados = total_testes
    tempo_total = "2min 15s"
    tempo_medio = "16,9s/teste"

    # Criar caixa de resumo
    summary_text = f"""Resumo da Execução:
• Total de testes: {total_testes}
• Testes aprovados: {testes_aprovados} (100%)
• Tempo total: {tempo_total} (média: {tempo_medio})
• Ambiente: Android Emulator (produção)
• Chamadas API: ~15 requisições
• Interações UI: ~40 (taps, texto, navegação)
• Operações Firebase: leitura/escrita favoritos"""

    # Adicionar resumo no canto inferior esquerdo
    ax.text(0.02, 0.02, summary_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='#d4edda', alpha=0.8, edgecolor='green', linewidth=2),
            family='monospace')

    # Legenda
    legend_text = "Legenda: Todos os testes aprovados com sucesso"
    ax.text(0.98, 0.02, legend_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='bottom',
            horizontalalignment='right',
            style='italic',
            bbox=dict(boxstyle='round', facecolor='#fff3cd', alpha=0.8, edgecolor='orange', linewidth=1))

    # Framework info
    framework_text = "Framework: Flutter integration_test + WidgetTester | Binding: IntegrationTestWidgetsFlutterBinding"
    ax.text(0.5, 0.02, framework_text,
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment='bottom',
            horizontalalignment='center',
            style='italic',
            color='gray')

    plt.tight_layout()

    written: list[Path] = []

    # Cópia com timestamp (histórico local)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    API_GRAPHS.mkdir(parents=True, exist_ok=True)
    timestamped = API_GRAPHS / f'e2e_test_results_table_{timestamp}.png'
    plt.savefig(timestamped, dpi=300, bbox_inches='tight', pad_inches=0.5)
    written.append(timestamped)
    print(f"✓ Tabela de testes E2E salva: {timestamped}")

    # PNG canônico da monografia (Tabela 4)
    if thesis:
        THESIS_TABLE_4.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(THESIS_TABLE_4, dpi=300, bbox_inches='tight', pad_inches=0.5)
        written.append(THESIS_TABLE_4)
        print(f"✓ Tabela 4 (monografia) atualizada: {THESIS_TABLE_4}")

    plt.close()
    return written


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera a tabela visual dos testes E2E (Tabela 4 da monografia)."
    )
    parser.add_argument(
        "--thesis",
        action="store_true",
        help=(
            "Também grava o PNG canônico em "
            "evaluation/02_graphs/tables/tabela-4_e2e_test_results_table.png"
        ),
    )
    args = parser.parse_args()

    print("=" * 80)
    print("GERANDO TABELA DE TESTES E2E")
    print("=" * 80)
    print()

    written = generate_e2e_test_table(thesis=args.thesis)

    print()
    print("=" * 80)
    print("✅ TABELA GERADA COM SUCESSO")
    print("=" * 80)
    for path in written:
        print(f"Arquivo: {path}")
    if not args.thesis:
        print()
        print("Dica: use --thesis para regenerar o PNG canônico da Tabela 4 na monografia.")
    print()
    print("A tabela inclui descrições detalhadas de cada teste,")
    print("explicando o que é testado e o que é validado.")
    print("Para atualizar os dados, edite a lista TESTES neste script.")


if __name__ == "__main__":
    main()
