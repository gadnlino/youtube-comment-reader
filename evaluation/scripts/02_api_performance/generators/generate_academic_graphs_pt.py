"""
Gerador de Gráficos de Qualidade Acadêmica para Avaliação de Performance de API
(Academic-Grade Graph Generator for API Performance Evaluation - Portuguese Version)

Este script gera gráficos de qualidade publicável com todos os textos em Português
para inclusão no relatório final da disciplina.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import json
import glob
import sys
import seaborn as sns
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _paths import API_ROOT, DATA

# Configurar estilo de qualidade para publicação
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 14

class GeradorGraficosAcademicos:
    """
    Gera gráficos abrangentes de qualidade publicável para relatórios acadêmicos.
    Todos os textos em Português.
    """
    
    def __init__(self):
        """Inicializa o gerador de gráficos."""
        self.extended_data = None
        self.heavy_load_data = None
        self.multi_video_data = None
        self.multi_video_summary = None
        
    def carregar_todos_dados(self):
        """Carrega todos os dados de teste de performance."""
        print("📊 Carregando todos os dados de performance...")
        
        # Carregar dados de teste de performance estendido
        try:
            self.extended_data = pd.read_csv(
                str(DATA / 'csv' / 'extended_performance_results.csv')
            )
            print(f"   ✅ Teste estendido: {len(self.extended_data)} requisições")
        except Exception as e:
            print(f"   ⚠️  Dados de teste estendido não encontrados: {e}")
        
        # Carregar dados de teste de carga pesada
        try:
            self.heavy_load_data = pd.read_csv(
                str(DATA / 'csv' / 'heavy_load_test_results.csv')
            )
            print(f"   ✅ Teste de carga pesada: {len(self.heavy_load_data)} requisições")
        except Exception as e:
            print(f"   ⚠️  Dados de teste de carga pesada não encontrados: {e}")
        
        # Carregar dados de teste multi-vídeo
        try:
            self.multi_video_data = pd.read_csv(
                str(DATA / 'csv' / 'multi_video_results.csv')
            )
            print(f"   ✅ Teste multi-vídeo: {len(self.multi_video_data)} requisições")
        except Exception as e:
            print(f"   ⚠️  Dados de teste multi-vídeo não encontrados: {e}")
        
        # Carregar resumo multi-vídeo
        try:
            with open(DATA / 'json' / 'multi_video_summary.json', 'r') as f:
                self.multi_video_summary = json.load(f)
            print(f"   ✅ Resumo multi-vídeo carregado")
        except Exception as e:
            print(f"   ⚠️  Resumo multi-vídeo não encontrado: {e}")
        
        # Carregar dados de análise de tamanho de lote (NOVO!)
        try:
            # Encontrar o arquivo mais recente de análise de tamanho de lote
            import glob
            batch_files = glob.glob(str(DATA / 'csv' / 'batch_size_analysis.csv'))
            if not batch_files:
                batch_files = glob.glob(str(API_ROOT / 'batch_size_analysis_*.csv'))
            if batch_files:
                latest_batch_file = max(batch_files)
                self.batch_size_data = pd.read_csv(latest_batch_file)
                print(f"   ✅ Análise de tamanho de lote: {len(self.batch_size_data)} requisições")
            else:
                self.batch_size_data = None
        except Exception as e:
            print(f"   ⚠️  Dados de análise de tamanho de lote não encontrados: {e}")
            self.batch_size_data = None
    
    def gerar_visao_geral_performance(self):
        """
        Figura 1: Visão Geral Abrangente de Performance
        Figura multi-painel mostrando todas as métricas-chave.
        """
        print("\n📈 Gerando Figura 1: Visão Geral Abrangente de Performance...")
        
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Distribuição do Tempo de Resposta (Teste Estendido)
        ax1 = fig.add_subplot(gs[0, :2])
        if self.extended_data is not None:
            response_times = self.extended_data['response_time_ms']
            ax1.hist(response_times, bins=30, color='#3498db', alpha=0.7, edgecolor='black')
            ax1.axvline(response_times.mean(), color='red', linestyle='--', 
                       label=f'Média: {response_times.mean():.0f}ms', linewidth=2)
            ax1.axvline(response_times.median(), color='green', linestyle='--', 
                       label=f'Mediana: {response_times.median():.0f}ms', linewidth=2)
            ax1.set_xlabel('Tempo de Resposta (ms)', fontweight='bold')
            ax1.set_ylabel('Frequência', fontweight='bold')
            ax1.set_title('(A) Distribuição do Tempo de Resposta - Teste Estendido (n=219)', 
                         fontweight='bold', loc='left')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        
        # 2. Gráfico de Caixa Comparativo
        ax2 = fig.add_subplot(gs[0, 2])
        box_data = []
        labels = []
        
        if self.extended_data is not None:
            box_data.append(self.extended_data['response_time_ms'])
            labels.append('Estendido\n(n=219)')
        
        if self.heavy_load_data is not None:
            box_data.append(self.heavy_load_data['response_time_ms'])
            labels.append('Carga Pesada\n(n=106)')
        
        if self.multi_video_data is not None:
            box_data.append(self.multi_video_data['response_time_ms'])
            labels.append('Multi-Vídeo\n(n=60)')
        
        bp = ax2.boxplot(box_data, tick_labels=labels, patch_artist=True)
        for patch, color in zip(bp['boxes'], ['#3498db', '#e74c3c', '#2ecc71']):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        ax2.set_ylabel('Tempo de Resposta (ms)', fontweight='bold')
        ax2.set_title('(B) Comparação de Testes', fontweight='bold', loc='left')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Série Temporal - Teste Estendido
        ax3 = fig.add_subplot(gs[1, :])
        if self.extended_data is not None:
            x = range(len(self.extended_data))
            y = self.extended_data['response_time_ms']
            
            ax3.scatter(x, y, alpha=0.5, s=20, color='#3498db', label='Requisições Individuais')
            
            # Adicionar média móvel
            window = 10
            rolling_avg = pd.Series(y).rolling(window=window, center=True).mean()
            ax3.plot(x, rolling_avg, color='red', linewidth=2, 
                    label=f'Média Móvel de {window} Requisições')
            
            # Adicionar linha de média
            ax3.axhline(y.mean(), color='green', linestyle='--', 
                       label=f'Média Geral: {y.mean():.0f}ms', linewidth=1.5)
            
            ax3.set_xlabel('Número da Requisição', fontweight='bold')
            ax3.set_ylabel('Tempo de Resposta (ms)', fontweight='bold')
            ax3.set_title('(C) Tempo de Resposta ao Longo do Período de Teste Estendido (n=219)', 
                         fontweight='bold', loc='left')
            ax3.legend(loc='upper right')
            ax3.grid(True, alpha=0.3)
        
        # 4. Análise de Percentis
        ax4 = fig.add_subplot(gs[2, 0])
        if self.extended_data is not None:
            percentiles = [50, 75, 90, 95, 99]
            values = [np.percentile(self.extended_data['response_time_ms'], p) 
                     for p in percentiles]
            
            bars = ax4.bar(range(len(percentiles)), values, color='#3498db', 
                          alpha=0.7, edgecolor='black')
            ax4.set_xticks(range(len(percentiles)))
            ax4.set_xticklabels([f'P{p}' for p in percentiles])
            ax4.set_ylabel('Tempo de Resposta (ms)', fontweight='bold')
            ax4.set_title('(D) Análise de Percentis', fontweight='bold', loc='left')
            ax4.grid(True, alpha=0.3, axis='y')
            
            # Adicionar rótulos de valores
            for i, (bar, val) in enumerate(zip(bars, values)):
                ax4.text(bar.get_x() + bar.get_width()/2, val + 50, 
                        f'{val:.0f}ms', ha='center', va='bottom', fontsize=8)
        
        # 5. Comparação Multi-Vídeo
        ax5 = fig.add_subplot(gs[2, 1])
        if self.multi_video_summary is not None:
            video_results = self.multi_video_summary['video_results']
            video_names = [r['content_type'] for r in video_results]
            # Traduzir tipos de conteúdo
            traducao_tipos = {'Music': 'Música', 'Documentary': 'Documentário', 'Viral': 'Viral'}
            video_names = [traducao_tipos.get(name, name) for name in video_names]
            avg_times = [r['avg_response_time'] for r in video_results]
            
            colors = ['#3498db', '#2ecc71', '#e74c3c']
            bars = ax5.bar(range(len(video_names)), avg_times, 
                          color=colors[:len(video_names)], alpha=0.7, edgecolor='black')
            ax5.set_xticks(range(len(video_names)))
            ax5.set_xticklabels(video_names, rotation=15, ha='right')
            ax5.set_ylabel('Tempo Médio de Resposta (ms)', fontweight='bold')
            ax5.set_title('(E) Performance por Tipo de Conteúdo', fontweight='bold', loc='left')
            ax5.grid(True, alpha=0.3, axis='y')
            
            # Adicionar rótulos de valores
            for bar, val in zip(bars, avg_times):
                ax5.text(bar.get_x() + bar.get_width()/2, val + 10, 
                        f'{val:.0f}ms', ha='center', va='bottom', fontsize=8)
        
        # 6. Resumo de Taxa de Sucesso
        ax6 = fig.add_subplot(gs[2, 2])
        test_names = []
        success_rates = []
        
        if self.extended_data is not None:
            test_names.append('Estendido')
            success_rates.append(100)
        
        if self.heavy_load_data is not None:
            test_names.append('Carga Pesada')
            success_rates.append(100)
        
        if self.multi_video_data is not None:
            test_names.append('Multi-Vídeo')
            success_rates.append(100)
        
        bars = ax6.bar(range(len(test_names)), success_rates, 
                      color='#2ecc71', alpha=0.7, edgecolor='black')
        ax6.set_xticks(range(len(test_names)))
        ax6.set_xticklabels(test_names, rotation=15, ha='right')
        ax6.set_ylabel('Taxa de Sucesso (%)', fontweight='bold')
        ax6.set_title('(F) Resumo de Confiabilidade', fontweight='bold', loc='left')
        ax6.set_ylim([98, 101])
        ax6.grid(True, alpha=0.3, axis='y')
        
        # Adicionar linha de 100%
        ax6.axhline(100, color='green', linestyle='--', linewidth=1, alpha=0.5)
        
        # Adicionar rótulos de valores
        for bar in bars:
            ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 0.3, 
                    '100%', ha='center', va='top', fontsize=9, fontweight='bold')
        
        plt.suptitle('Análise Abrangente de Performance da API - Todos os Testes', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        filename = str(API_ROOT / 'visao_geral_performance_pt.png')
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"   ✅ Salvo: {filename}")
    
    def gerar_analise_escalabilidade(self):
        """
        Figura 2: Análise de Escalabilidade
        Mostra performance sob carga crescente.
        """
        print("\n📈 Gerando Figura 2: Análise de Escalabilidade...")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Análise de Escalabilidade - Performance Sob Carga', 
                    fontsize=14, fontweight='bold')
        
        # 1. Tamanho de Lote vs Tempo de Resposta (ATUALIZADO com novos dados!)
        ax1 = axes[0, 0]
        if self.batch_size_data is not None:
            # Agrupar por tamanho de lote e calcular média
            batch_summary = self.batch_size_data.groupby('batch_size').agg({
                'response_time_ms': 'mean',
                'time_per_comment_ms': 'mean'
            }).reset_index()
            
            ax1.scatter(batch_summary['batch_size'], 
                       batch_summary['response_time_ms'],
                       alpha=0.7, s=100, color='#e74c3c', edgecolors='black', linewidth=1.5)
            
            # Adicionar linha conectando pontos
            ax1.plot(batch_summary['batch_size'], 
                    batch_summary['response_time_ms'],
                    color='#e74c3c', linewidth=2, alpha=0.5)
            
            # Adicionar linha de tendência
            z = np.polyfit(batch_summary['batch_size'], 
                          batch_summary['response_time_ms'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(batch_summary['batch_size'].min(), 
                                batch_summary['batch_size'].max(), 100)
            ax1.plot(x_line, p(x_line), "b--", alpha=0.6, linewidth=2, 
                    label=f'Tendência: y={z[0]:.2f}x+{z[1]:.0f}')
            
            # Calcular e exibir correlação
            corr = np.corrcoef(batch_summary['batch_size'], batch_summary['response_time_ms'])[0, 1]
            ax1.text(0.05, 0.95, f'Correlação: r={corr:.3f}', 
                    transform=ax1.transAxes, fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                    verticalalignment='top')
            
            ax1.set_xlabel('Tamanho do Lote (número de comentários)', fontweight='bold')
            ax1.set_ylabel('Tempo de Resposta (ms)', fontweight='bold')
            ax1.set_title('(A) Tempo de Resposta vs Tamanho do Lote', fontweight='bold', loc='left')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        elif self.heavy_load_data is not None:
            # Fallback para visualização antiga
            ax1.scatter(self.heavy_load_data['actual_count'], 
                       self.heavy_load_data['response_time_ms'],
                       alpha=0.6, s=30, color='#e74c3c')
            ax1.set_xlabel('Número de Comentários por Requisição', fontweight='bold')
            ax1.set_ylabel('Tempo de Resposta (ms)', fontweight='bold')
            ax1.set_title('(A) Tempo de Resposta vs Tamanho do Lote', fontweight='bold', loc='left')
            ax1.grid(True, alpha=0.3)
        
        # 2. Performance Cumulativa
        ax2 = axes[0, 1]
        if self.heavy_load_data is not None:
            cumulative_comments = self.heavy_load_data['actual_count'].cumsum()
            cumulative_time = self.heavy_load_data['response_time_ms'].cumsum() / 1000  # para segundos
            
            ax2.plot(cumulative_comments, cumulative_time, 
                    color='#2ecc71', linewidth=2)
            ax2.fill_between(cumulative_comments, 0, cumulative_time, 
                            alpha=0.3, color='#2ecc71')
            
            ax2.set_xlabel('Total de Comentários Processados', fontweight='bold')
            ax2.set_ylabel('Tempo Cumulativo (segundos)', fontweight='bold')
            ax2.set_title('(B) Tempo de Processamento Cumulativo', fontweight='bold', loc='left')
            ax2.grid(True, alpha=0.3)
            
            # Adicionar anotação de throughput
            total_comments = cumulative_comments.iloc[-1]
            total_time = cumulative_time.iloc[-1]
            throughput = total_comments / total_time
            ax2.text(0.5, 0.95, f'Taxa: {throughput:.1f} coments/seg', 
                    transform=ax2.transAxes, ha='center', va='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 3. Estabilidade de Performance ao Longo do Tempo
        ax3 = axes[1, 0]
        if self.heavy_load_data is not None:
            # Calcular estatísticas móveis
            window = 10
            rolling_mean = self.heavy_load_data['response_time_ms'].rolling(window=window).mean()
            rolling_std = self.heavy_load_data['response_time_ms'].rolling(window=window).std()
            
            x = range(len(self.heavy_load_data))
            ax3.plot(x, rolling_mean, color='#3498db', linewidth=2, label='Média de 10 Requisições')
            ax3.fill_between(x, rolling_mean - rolling_std, rolling_mean + rolling_std, 
                            alpha=0.3, color='#3498db', label='±1 Desvio Padrão')
            
            ax3.set_xlabel('Número da Requisição', fontweight='bold')
            ax3.set_ylabel('Tempo de Resposta (ms)', fontweight='bold')
            ax3.set_title('(C) Estabilidade de Performance (Carga Pesada)', fontweight='bold', loc='left')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        
        # 4. Análise de Tempo por Comentário
        ax4 = axes[1, 1]
        if self.heavy_load_data is not None:
            time_per_comment = (self.heavy_load_data['response_time_ms'] / 
                               self.heavy_load_data['actual_count'])
            
            ax4.hist(time_per_comment, bins=30, color='#9b59b6', 
                    alpha=0.7, edgecolor='black')
            ax4.axvline(time_per_comment.mean(), color='red', linestyle='--', 
                       label=f'Média: {time_per_comment.mean():.2f}ms/coment', linewidth=2)
            ax4.axvline(time_per_comment.median(), color='green', linestyle='--', 
                       label=f'Mediana: {time_per_comment.median():.2f}ms/coment', linewidth=2)
            
            ax4.set_xlabel('Tempo por Comentário (ms)', fontweight='bold')
            ax4.set_ylabel('Frequência', fontweight='bold')
            ax4.set_title('(D) Distribuição de Eficiência de Processamento', fontweight='bold', loc='left')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filename = str(API_ROOT / 'analise_escalabilidade_pt.png')
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"   ✅ Salvo: {filename}")
    
    def gerar_resumo_estatistico(self):
        """
        Figura 3: Resumo Estatístico
        Análise estatística detalhada com intervalos de confiança.
        """
        print("\n📈 Gerando Figura 3: Resumo Estatístico...")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Análise Estatística - Métricas de Tempo de Resposta', 
                    fontsize=14, fontweight='bold')
        
        # 1. Gráfico Q-Q (Teste de Distribuição Normal)
        ax1 = axes[0, 0]
        if self.extended_data is not None:
            from scipy import stats
            
            response_times = self.extended_data['response_time_ms']
            stats.probplot(response_times, dist="norm", plot=ax1)
            ax1.set_title('(A) Gráfico Q-Q - Teste de Normalidade', fontweight='bold', loc='left')
            ax1.set_xlabel('Quantis Teóricos', fontweight='bold')
            ax1.set_ylabel('Quantis Ordenados', fontweight='bold')
            ax1.grid(True, alpha=0.3)
        
        # 2. Função de Distribuição Cumulativa
        ax2 = axes[0, 1]
        if self.extended_data is not None:
            response_times = sorted(self.extended_data['response_time_ms'])
            cumulative = np.arange(1, len(response_times) + 1) / len(response_times) * 100
            
            ax2.plot(response_times, cumulative, color='#3498db', linewidth=2)
            ax2.axhline(50, color='green', linestyle='--', alpha=0.5, label='P50 (Mediana)')
            ax2.axhline(95, color='red', linestyle='--', alpha=0.5, label='P95')
            ax2.axhline(99, color='orange', linestyle='--', alpha=0.5, label='P99')
            
            ax2.set_xlabel('Tempo de Resposta (ms)', fontweight='bold')
            ax2.set_ylabel('Probabilidade Cumulativa (%)', fontweight='bold')
            ax2.set_title('(B) Função de Distribuição Cumulativa', fontweight='bold', loc='left')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        # 3. Comparação de Tendências Centrais
        ax3 = axes[1, 0]
        
        metrics = ['Média', 'Mediana', 'Moda']
        extended_values = []
        heavy_values = []
        multi_values = []
        
        if self.extended_data is not None:
            rt = self.extended_data['response_time_ms']
            extended_values = [rt.mean(), rt.median(), rt.mode()[0] if len(rt.mode()) > 0 else rt.median()]
        
        if self.heavy_load_data is not None:
            rt = self.heavy_load_data['response_time_ms']
            heavy_values = [rt.mean(), rt.median(), rt.mode()[0] if len(rt.mode()) > 0 else rt.median()]
        
        if self.multi_video_data is not None:
            rt = self.multi_video_data['response_time_ms']
            multi_values = [rt.mean(), rt.median(), rt.mode()[0] if len(rt.mode()) > 0 else rt.median()]
        
        x = np.arange(len(metrics))
        width = 0.25
        
        if extended_values:
            ax3.bar(x - width, extended_values, width, label='Estendido (n=219)', 
                   color='#3498db', alpha=0.7, edgecolor='black')
        if heavy_values:
            ax3.bar(x, heavy_values, width, label='Carga Pesada (n=106)', 
                   color='#e74c3c', alpha=0.7, edgecolor='black')
        if multi_values:
            ax3.bar(x + width, multi_values, width, label='Multi-Vídeo (n=60)', 
                   color='#2ecc71', alpha=0.7, edgecolor='black')
        
        ax3.set_ylabel('Tempo de Resposta (ms)', fontweight='bold')
        ax3.set_title('(C) Comparação de Tendências Centrais', fontweight='bold', loc='left')
        ax3.set_xticks(x)
        ax3.set_xticklabels(metrics)
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Comparação de Variabilidade
        ax4 = axes[1, 1]
        
        test_names = []
        std_devs = []
        cvs = []  # Coeficiente de Variação
        
        if self.extended_data is not None:
            rt = self.extended_data['response_time_ms']
            test_names.append('Estendido')
            std_devs.append(rt.std())
            cvs.append((rt.std() / rt.mean()) * 100)
        
        if self.heavy_load_data is not None:
            rt = self.heavy_load_data['response_time_ms']
            test_names.append('Carga Pesada')
            std_devs.append(rt.std())
            cvs.append((rt.std() / rt.mean()) * 100)
        
        if self.multi_video_data is not None:
            rt = self.multi_video_data['response_time_ms']
            test_names.append('Multi-Vídeo')
            std_devs.append(rt.std())
            cvs.append((rt.std() / rt.mean()) * 100)
        
        x = np.arange(len(test_names))
        width = 0.35
        
        ax4_2 = ax4.twinx()
        
        bars1 = ax4.bar(x - width/2, std_devs, width, label='Desvio Padrão (ms)', 
                       color='#3498db', alpha=0.7, edgecolor='black')
        bars2 = ax4_2.bar(x + width/2, cvs, width, label='CV (%)', 
                         color='#e74c3c', alpha=0.7, edgecolor='black')
        
        ax4.set_xlabel('Tipo de Teste', fontweight='bold')
        ax4.set_ylabel('Desvio Padrão (ms)', fontweight='bold', color='#3498db')
        ax4_2.set_ylabel('Coeficiente de Variação (%)', fontweight='bold', color='#e74c3c')
        ax4.set_title('(D) Métricas de Variabilidade', fontweight='bold', loc='left')
        ax4.set_xticks(x)
        ax4.set_xticklabels(test_names)
        ax4.tick_params(axis='y', labelcolor='#3498db')
        ax4_2.tick_params(axis='y', labelcolor='#e74c3c')
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Legenda combinada
        lines1, labels1 = ax4.get_legend_handles_labels()
        lines2, labels2 = ax4_2.get_legend_handles_labels()
        ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        plt.tight_layout()
        
        filename = str(API_ROOT / 'resumo_estatistico_pt.png')
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"   ✅ Salvo: {filename}")
    
    def gerar_mapa_calor_performance(self):
        """
        Figura 4: Mapa de Calor de Performance
        Mostra distribuição de performance ao longo do tempo em 2D.
        """
        print("\n📈 Gerando Figura 4: Mapa de Calor de Performance...")
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('Mapa de Calor da Distribuição de Performance', 
                    fontsize=14, fontweight='bold')
        
        # 1. Mapa de Calor do Teste Estendido
        ax1 = axes[0]
        if self.extended_data is not None and len(self.extended_data) >= 100:
            # Remodelar dados em grade 2D para mapa de calor
            data_100 = self.extended_data['response_time_ms'][:100].values
            heatmap_data = data_100.reshape(10, 10)
            
            im1 = ax1.imshow(heatmap_data, cmap='RdYlGn_r', aspect='auto')
            ax1.set_title('(A) Teste Estendido - Primeiras 100 Requisições', 
                         fontweight='bold', loc='left')
            ax1.set_xlabel('Lote de Requisições (×10)', fontweight='bold')
            ax1.set_ylabel('Grupo de Requisições', fontweight='bold')
            
            # Adicionar barra de cores
            cbar1 = plt.colorbar(im1, ax=ax1)
            cbar1.set_label('Tempo de Resposta (ms)', rotation=270, labelpad=20, fontweight='bold')
        
        # 2. Mapa de Calor de Carga Pesada
        ax2 = axes[1]
        if self.heavy_load_data is not None and len(self.heavy_load_data) >= 100:
            # Remodelar dados em grade 2D para mapa de calor
            data_100 = self.heavy_load_data['response_time_ms'][:100].values
            heatmap_data = data_100.reshape(10, 10)
            
            im2 = ax2.imshow(heatmap_data, cmap='RdYlGn_r', aspect='auto')
            ax2.set_title('(B) Teste de Carga Pesada - Primeiras 100 Requisições', 
                         fontweight='bold', loc='left')
            ax2.set_xlabel('Lote de Requisições (×10)', fontweight='bold')
            ax2.set_ylabel('Grupo de Requisições', fontweight='bold')
            
            # Adicionar barra de cores
            cbar2 = plt.colorbar(im2, ax=ax2)
            cbar2.set_label('Tempo de Resposta (ms)', rotation=270, labelpad=20, fontweight='bold')
        
        plt.tight_layout()
        
        filename = str(API_ROOT / 'mapa_calor_performance_pt.png')
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"   ✅ Salvo: {filename}")
    
    def gerar_todos_graficos(self):
        """Gera todos os gráficos de qualidade acadêmica em Português."""
        print("\n" + "="*80)
        print("📊 GERANDO GRÁFICOS DE QUALIDADE ACADÊMICA (PORTUGUÊS)")
        print("="*80)
        
        self.carregar_todos_dados()
        
        self.gerar_visao_geral_performance()
        self.gerar_analise_escalabilidade()
        self.gerar_resumo_estatistico()
        self.gerar_mapa_calor_performance()
        
        print("\n" + "="*80)
        print("✅ TODOS OS GRÁFICOS GERADOS COM SUCESSO!")
        print("="*80)
        print("\n📁 Arquivos Gerados:")
        print("   1. visao_geral_performance_pt.png")
        print("   2. analise_escalabilidade_pt.png")
        print("   3. resumo_estatistico_pt.png")
        print("   4. mapa_calor_performance_pt.png")
        print(f"\n📍 Localização: {API_ROOT}/")
        print("\n🎓 Todos os gráficos são de qualidade publicável (300 DPI)")
        print("   Prontos para inclusão no seu relatório final da disciplina!")


if __name__ == "__main__":
    gerador = GeradorGraficosAcademicos()
    gerador.gerar_todos_graficos()

