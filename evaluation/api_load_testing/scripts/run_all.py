#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Principal - Executa Todos os Testes de Performance

Dispara todas as baterias de teste e gera um resumo final.
"""

import os
import sys
from datetime import datetime
from typing import Dict, Any
import json

# Adicionar o diretório atual ao path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import setup_logging
from videos import run_video_tests
from comments import run_comment_tests
from stability import run_stability_test

# Configurar logging global
logger = setup_logging('perf_test.log')


def generate_summary(video_results: Dict[str, Any], 
                    comment_results: Dict[str, Any],
                    stability_results: Dict[str, Any]) -> str:
    """
    Gera resumo textual dos resultados de todos os testes.
    
    Returns:
        String com o resumo formatado
    """
    summary_lines = []
    summary_lines.append("="*80)
    summary_lines.append("RESUMO EXECUTIVO - TESTES DE PERFORMANCE DA API")
    summary_lines.append("="*80)
    summary_lines.append(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary_lines.append("")
    
    # 1. Listagem de Vídeos
    if video_results and 'metrics' in video_results:
        summary_lines.append("1. LISTAGEM DE VÍDEOS")
        summary_lines.append("-"*80)
        summary_lines.append("")
        summary_lines.append("Tempo médio e P95 por cenário:")
        summary_lines.append("")
        
        for scenario, metrics in video_results['metrics'].items():
            summary_lines.append(f"  {scenario}:")
            summary_lines.append(f"    Média: {metrics['mean']:.0f}ms")
            summary_lines.append(f"    P95:   {metrics['p95']:.0f}ms")
            summary_lines.append(f"    Sucessos: {metrics['success_count']}/{metrics['count']}")
            summary_lines.append("")
        
        # Comparações
        if len(video_results['metrics']) > 1:
            summary_lines.append("Comparações:")
            scenarios = list(video_results['metrics'].keys())
            means = [video_results['metrics'][s]['mean'] for s in scenarios]
            fastest = scenarios[means.index(min(means))]
            slowest = scenarios[means.index(max(means))]
            summary_lines.append(f"  Cenário mais rápido: {fastest} ({min(means):.0f}ms)")
            summary_lines.append(f"  Cenário mais lento: {slowest} ({max(means):.0f}ms)")
            summary_lines.append(f"  Diferença: {max(means) - min(means):.0f}ms ({((max(means)/min(means)-1)*100):.1f}%)")
            summary_lines.append("")
    
    # 2. Listagem de Comentários
    if comment_results and 'metrics' in comment_results:
        summary_lines.append("2. LISTAGEM DE COMENTÁRIOS")
        summary_lines.append("-"*80)
        summary_lines.append("")
        summary_lines.append("Tempo médio e P95 por volume de comentários:")
        summary_lines.append("")
        
        for volume, metrics in comment_results['metrics'].items():
            summary_lines.append(f"  {volume}:")
            summary_lines.append(f"    Média: {metrics['mean']:.0f}ms")
            summary_lines.append(f"    P95:   {metrics['p95']:.0f}ms")
            summary_lines.append(f"    Sucessos: {metrics['success_count']}/{metrics['count']}")
            summary_lines.append("")
        
        # Comparações
        if len(comment_results['metrics']) > 1:
            summary_lines.append("Impacto do volume de comentários:")
            volumes = list(comment_results['metrics'].keys())
            means = [comment_results['metrics'][v]['mean'] for v in volumes]
            fastest = volumes[means.index(min(means))]
            slowest = volumes[means.index(max(means))]
            summary_lines.append(f"  Volume mais rápido: {fastest} ({min(means):.0f}ms)")
            summary_lines.append(f"  Volume mais lento: {slowest} ({max(means):.0f}ms)")
            summary_lines.append(f"  Diferença: {max(means) - min(means):.0f}ms ({((max(means)/min(means)-1)*100):.1f}%)")
            summary_lines.append("")
    
    # 3. Estabilidade Temporal
    if stability_results and 'metrics' in stability_results:
        summary_lines.append("3. ESTABILIDADE SOB CARGA")
        summary_lines.append("-"*80)
        summary_lines.append("")
        metrics = stability_results['metrics']
        
        # TPS se disponível
        if 'tps' in metrics:
            summary_lines.append(f"  TPS (Transactions Per Second): {metrics['tps']:.2f}")
            summary_lines.append(f"  Requisições por minuto: {metrics['tps']*60:.1f}")
            summary_lines.append(f"  Requisições por hora: {metrics['tps']*3600:.0f}")
            summary_lines.append("")
        
        summary_lines.append(f"  Total de requisições: {metrics.get('total_requests', metrics['count'])}")
        summary_lines.append(f"  Tempo total: {metrics.get('total_time_seconds', 0)/60:.1f} minutos")
        summary_lines.append(f"  Média: {metrics['mean']:.0f}ms")
        summary_lines.append(f"  Mediana: {metrics['median']:.0f}ms")
        summary_lines.append(f"  P95: {metrics['p95']:.0f}ms")
        summary_lines.append(f"  Mínimo: {metrics['min']:.0f}ms")
        summary_lines.append(f"  Máximo: {metrics['max']:.0f}ms")
        summary_lines.append(f"  Desvio Padrão: {metrics['std']:.0f}ms")
        summary_lines.append(f"  Sucessos: {metrics['success_count']}/{metrics['count']}")
        summary_lines.append("")
        
        # Análise de estabilidade
        cv = (metrics['std'] / metrics['mean'] * 100) if metrics['mean'] > 0 else 0
        summary_lines.append("Análise de Estabilidade:")
        summary_lines.append(f"  Coeficiente de Variação: {cv:.1f}%")
        if cv < 20:
            summary_lines.append("  ✅ Performance estável (CV < 20%)")
        elif cv < 40:
            summary_lines.append("  ⚠️  Performance moderadamente variável (20% < CV < 40%)")
        else:
            summary_lines.append("  ❌ Performance instável (CV > 40%)")
        summary_lines.append("")
        
        # Análise de TPS
        if 'tps' in metrics:
            tps = metrics['tps']
            summary_lines.append("Análise de Throughput (TPS):")
            summary_lines.append(f"  TPS médio: {tps:.2f} transações/segundo")
            summary_lines.append(f"  Capacidade estimada: {tps*3600:.0f} requisições/hora")
            if tps >= 1.0:
                summary_lines.append("  ✅ Throughput excelente (≥ 1 TPS)")
            elif tps >= 0.5:
                summary_lines.append("  ✅ Throughput bom (≥ 0.5 TPS)")
            elif tps >= 0.1:
                summary_lines.append("  ⚠️  Throughput moderado (≥ 0.1 TPS)")
            else:
                summary_lines.append("  ❌ Throughput baixo (< 0.1 TPS)")
            summary_lines.append("")
    
    # Conclusões Gerais
    summary_lines.append("="*80)
    summary_lines.append("CONCLUSÕES GERAIS")
    summary_lines.append("="*80)
    summary_lines.append("")
    
    all_means = []
    if video_results and 'metrics' in video_results:
        all_means.extend([m['mean'] for m in video_results['metrics'].values()])
    if comment_results and 'metrics' in comment_results:
        all_means.extend([m['mean'] for m in comment_results['metrics'].values()])
    if stability_results and 'metrics' in stability_results:
        all_means.append(stability_results['metrics']['mean'])
    
    if all_means:
        overall_mean = sum(all_means) / len(all_means)
        summary_lines.append(f"Tempo médio geral (todos os testes): {overall_mean:.0f}ms")
        summary_lines.append("")
        
        # Verificar se está dentro de limites aceitáveis
        if overall_mean < 1000:
            summary_lines.append("✅ Performance geral EXCELENTE (< 1000ms)")
        elif overall_mean < 2000:
            summary_lines.append("✅ Performance geral BOA (< 2000ms)")
        elif overall_mean < 3000:
            summary_lines.append("⚠️  Performance geral ACEITÁVEL (< 3000ms)")
        else:
            summary_lines.append("❌ Performance geral PRECISA DE MELHORIAS (> 3000ms)")
        summary_lines.append("")
    
    summary_lines.append("="*80)
    
    return "\n".join(summary_lines)


def main():
    """Função principal que executa todos os testes."""
    logger.info("="*80)
    logger.info("EXECUÇÃO COMPLETA DOS TESTES DE PERFORMANCE")
    logger.info("="*80)
    logger.info(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("")
    logger.info("📋 LOGS SERÃO SALVOS EM: perf_test.log")
    logger.info("   Você pode acompanhar o progresso verificando este arquivo")
    logger.info("")
    
    # Criar diretórios necessários
    os.makedirs('results', exist_ok=True)
    os.makedirs('graphs', exist_ok=True)
    logger.info("✓ Diretórios criados: results/, graphs/")
    
    results = {
        'video': {},
        'comment': {},
        'stability': {}
    }
    
    # 1. Testes de Listagem de Vídeos
    logger.info("\n" + "="*80)
    logger.info("INICIANDO: Testes de Listagem de Vídeos")
    logger.info("="*80)
    try:
        results['video'] = run_video_tests()
        logger.info("✅ Testes de vídeos concluídos com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro nos testes de vídeos: {e}")
        import traceback
        logger.error(traceback.format_exc())
    
    # 2. Testes de Listagem de Comentários
    logger.info("\n\n" + "="*80)
    logger.info("INICIANDO: Testes de Listagem de Comentários")
    logger.info("="*80)
    try:
        results['comment'] = run_comment_tests()
        logger.info("✅ Testes de comentários concluídos com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro nos testes de comentários: {e}")
        import traceback
        logger.error(traceback.format_exc())
    
    # 3. Teste de Estabilidade
    logger.info("\n\n" + "="*80)
    logger.info("INICIANDO: Teste de Estabilidade Temporal")
    logger.info("="*80)
    logger.info("⚠️  ATENÇÃO: Este teste pode levar algum tempo!")
    logger.info("  Duração configurada: 10 minutos")
    logger.info("  Você pode acompanhar o progresso no arquivo perf_test.log")
    
    # Executar automaticamente (sem prompt interativo)
    try:
        results['stability'] = run_stability_test()
        logger.info("✅ Teste de estabilidade concluído com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro no teste de estabilidade: {e}")
        import traceback
        logger.error(traceback.format_exc())
    
    # Gerar resumo
    logger.info("\n\n" + "="*80)
    logger.info("GERANDO RESUMO EXECUTIVO...")
    logger.info("="*80)
    
    summary_text = generate_summary(
        results['video'],
        results['comment'],
        results['stability']
    )
    
    # Salvar resumo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    summary_file = f'results/perf_summary_{timestamp}.txt'
    summary_json_file = f'results/perf_summary_{timestamp}.json'
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_text)
    
    # Salvar também em JSON para fácil processamento
    summary_data = {
        'timestamp': datetime.now().isoformat(),
        'video_tests': results['video'],
        'comment_tests': results['comment'],
        'stability_test': results['stability']
    }
    
    with open(summary_json_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    # Exibir resumo
    logger.info(summary_text)
    
    logger.info("\n" + "="*80)
    logger.info("✅ TODOS OS TESTES CONCLUÍDOS")
    logger.info("="*80)
    logger.info(f"Resumo salvo em:")
    logger.info(f"  - {summary_file}")
    logger.info(f"  - {summary_json_file}")
    logger.info("")
    logger.info("Este resumo pode ser usado como base para a seção de avaliação")
    logger.info("de desempenho da monografia.")
    logger.info("")
    logger.info("📄 Todos os logs foram salvos em: perf_test.log")


if __name__ == "__main__":
    main()

