#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validação do Modelo com Dataset AiresPucrs/sentiment-analysis-pt (Português)

Este script valida o modelo TF-IDF + Logistic Regression usando o dataset
AiresPucrs/sentiment-analysis-pt do Hugging Face como validação independente.

Este dataset possui avaliações de filmes em português com 2 classes (positivo/negativo).

O script utiliza a Lambda URL da API de análise de sentimento.
"""

import pandas as pd
import json
import time
import os
import requests
from datetime import datetime
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

try:
    from datasets import load_dataset
    DATASETS_AVAILABLE = True
except ImportError:
    DATASETS_AVAILABLE = False
    print("⚠️  Biblioteca 'datasets' não instalada. Execute: pip install -r evaluation/requirements.txt")

# Configuration
SAMPLE_SIZE = None  # Usar dataset completo balanceado
RANDOM_STATE = 42
BATCH_SIZE = 100

# Lambda URL da API de análise de sentimento
SENTIMENT_API_URL = os.environ.get('SENTIMENT_ANALYSIS_API_URL', '')
SENTIMENT_API_KEY = os.environ.get('SENTIMENT_ANALYSIS_API_KEY', '')

def load_airespucrs_dataset(sample_size=None):
    """
    Carrega o dataset AiresPucrs/sentiment-analysis-pt do Hugging Face.
    """
    print("📊 Carregando dataset AiresPucrs/sentiment-analysis-pt...")
    
    if not DATASETS_AVAILABLE:
        raise ImportError("Biblioteca 'datasets' não está instalada. Execute: pip install -r evaluation/requirements.txt")
    
    try:
        print("📥 Baixando dataset do Hugging Face...")
        dataset = load_dataset("AiresPucrs/sentiment-analysis-pt")
        
        # Verificar estrutura do dataset
        print(f"✅ Dataset carregado!")
        print(f"   Divisões disponíveis: {list(dataset.keys())}")
        
        # Usar 'train' ou a primeira divisão disponível
        split_name = 'train' if 'train' in dataset else list(dataset.keys())[0]
        df = dataset[split_name].to_pandas()
        
        print(f"✅ Dataset convertido para DataFrame! Shape: {df.shape}")
        print(f"   Colunas: {df.columns.tolist()}")
        
        # Identificar colunas
        text_col = 'text' if 'text' in df.columns else df.columns[0]
        label_col = 'label' if 'label' in df.columns else df.columns[1]
        
        print(f"   Coluna de texto: {text_col}")
        print(f"   Coluna de label: {label_col}")
        
        # Verificar labels
        print(f"\n📊 Distribuição de labels:")
        print(df[label_col].value_counts())
        print()
        
        # Analisar exemplos para determinar mapeamento
        print("🔍 Analisando exemplos para determinar mapeamento de labels...")
        
        # Pegar alguns exemplos de cada label
        label_0_examples = df[df[label_col] == 0][text_col].head(10).tolist()
        label_1_examples = df[df[label_col] == 1][text_col].head(10).tolist()
        
        # Palavras-chave para análise
        negative_words = ['ruim', 'péssimo', 'horrível', 'odeio', 'triste', 'deprimido', 'raiva', 'ódio', 'mal', 'não gostei', 'desapontado', 'chato', 'entediante', 'terrível']
        positive_words = ['bom', 'ótimo', 'excelente', 'maravilhoso', 'feliz', 'gostei', 'adoro', 'amo', 'perfeito', 'incrível', 'recomendo', 'divertido', 'engraçado', 'fantástico']
        
        label_0_text = ' '.join([str(ex).lower() for ex in label_0_examples])
        label_1_text = ' '.join([str(ex).lower() for ex in label_1_examples])
        
        label_0_negative_count = sum(1 for word in negative_words if word in label_0_text)
        label_0_positive_count = sum(1 for word in positive_words if word in label_0_text)
        label_1_negative_count = sum(1 for word in negative_words if word in label_1_text)
        label_1_positive_count = sum(1 for word in positive_words if word in label_1_text)
        
        print(f"📊 Análise de palavras-chave:")
        print(f"  Label 0: {label_0_negative_count} negativas, {label_0_positive_count} positivas")
        print(f"  Label 1: {label_1_negative_count} negativas, {label_1_positive_count} positivas")
        
        # Determinar mapeamento usando razão
        label_0_ratio = label_0_positive_count / (label_0_negative_count + 1)
        label_1_ratio = label_1_positive_count / (label_1_negative_count + 1)
        
        if label_1_ratio > label_0_ratio:
            label_map = {0: 'NEGATIVE', 1: 'POSITIVE'}
            print(f"  ✅ Mapeamento: 0 → NEGATIVE, 1 → POSITIVE (razão: label0={label_0_ratio:.2f}, label1={label_1_ratio:.2f})")
        else:
            label_map = {0: 'POSITIVE', 1: 'NEGATIVE'}
            print(f"  ✅ Mapeamento: 0 → POSITIVE, 1 → NEGATIVE (razão: label0={label_0_ratio:.2f}, label1={label_1_ratio:.2f})")
        
        # Aplicar mapeamento
        df['sentiment_label'] = df[label_col].map(label_map)
        
        # Limpar dados
        df = df.dropna(subset=[text_col, 'sentiment_label'])
        df = df[df[text_col].notna()].copy()
        df = df[df[text_col].astype(str).str.strip() != ''].copy()
        
        print(f"\n✅ Dataset processado! Shape final: {df.shape}")
        print(f"📊 Distribuição de sentimentos:")
        print(df['sentiment_label'].value_counts())
        print()
        
        # Balancear dataset
        sentiment_counts = df['sentiment_label'].value_counts()
        min_class_size = sentiment_counts.min()
        
        if sample_size is not None:
            samples_per_class = min(sample_size // len(sentiment_counts), min_class_size)
        else:
            # Usar o maior tamanho balanceado possível
            samples_per_class = min_class_size
        
        print(f"📊 Balanceando dataset: {samples_per_class:,} amostras por classe")
        
        sampled_df = pd.DataFrame()
        for label in sentiment_counts.index:
            class_df = df[df['sentiment_label'] == label]
            sampled_df = pd.concat([sampled_df, class_df.sample(n=samples_per_class, random_state=RANDOM_STATE)])
        
        df = sampled_df.reset_index(drop=True)
        df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)  # Shuffle
        
        print(f"   Total balanceado: {len(df):,} amostras")
        print(f"📊 Distribuição final:")
        print(df['sentiment_label'].value_counts())
        print()
        
        return df, text_col
        
    except Exception as e:
        print(f"❌ Erro ao carregar dataset: {e}")
        import traceback
        traceback.print_exc()
        raise

def call_sentiment_api(comments_batch, api_url, api_key=None, retries=3):
    """Chama a API de análise de sentimento via Lambda URL."""
    payload = {
        'comments': comments_batch,
        'model_name': 'tfidf'
    }
    
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['x-api-key'] = api_key
    
    last_error = None
    for attempt in range(retries):
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json(), None
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                return None, last_error
    
    return None, last_error

def calculate_metrics(y_true, y_pred, labels):
    """Calcula métricas de avaliação."""
    accuracy = accuracy_score(y_true, y_pred)
    
    # Calcular métricas por classe
    precision = precision_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    
    # Matriz de confusão
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    # Classification report
    report = classification_report(y_true, y_pred, labels=labels, zero_division=0, output_dict=True)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm.tolist(),
        'classification_report': report,
        'labels': labels
    }

def main():
    """Função principal."""
    print("=" * 80)
    print("VALIDAÇÃO DO MODELO - AIRESPUCRS/SENTIMENT-ANALYSIS-PT (PORTUGUÊS)")
    print("=" * 80)
    print()
    
    # Verificar configuração da API
    global SENTIMENT_API_URL, SENTIMENT_API_KEY
    
    if not SENTIMENT_API_URL:
        print("⚠️  SENTIMENT_ANALYSIS_API_URL não configurada.")
        print("   Configure via variável de ambiente ou forneça no prompt:")
        api_url = input("   URL da API: ").strip()
        if not api_url:
            print("❌ URL da API é obrigatória. Abortando.")
            return
        SENTIMENT_API_URL = api_url
    
    if not SENTIMENT_API_KEY:
        print("⚠️  SENTIMENT_ANALYSIS_API_KEY não configurada.")
        api_key = input("   API Key: ").strip()
        if not api_key:
            print("❌ API Key é obrigatória. Abortando.")
            return
        SENTIMENT_API_KEY = api_key
    
    # Carregar dataset
    try:
        df, text_col = load_airespucrs_dataset(sample_size=SAMPLE_SIZE)
    except Exception as e:
        print(f"❌ Erro ao carregar dataset: {e}")
        return
    
    print(f"📊 Dataset carregado com sucesso!")
    print(f"   Total de amostras: {len(df):,}")
    print(f"   Coluna de texto: {text_col}")
    print()
    
    # Obter predições da API
    print("🔄 Obtendo predições da API...")
    print(f"   Processando {len(df):,} amostras em lotes de {BATCH_SIZE}...")
    
    predictions = []
    start_time = time.time()
    
    for i in range(0, len(df), BATCH_SIZE):
        batch = df.iloc[i:i+BATCH_SIZE]
        
        # Preparar lote de comentários no formato esperado pela API
        comments_batch = []
        for idx, (_, row) in enumerate(batch.iterrows()):
            comments_batch.append({
                'id': f'review_{i + idx}',
                'text': str(row[text_col]),
                'videoTitle': None
            })
        
        # Chamar API
        results, error = call_sentiment_api(comments_batch, SENTIMENT_API_URL, SENTIMENT_API_KEY)
        
        if results is None:
            print(f"    ⚠️  Erro na API: {error}")
            # Preencher com UNKNOWN em caso de erro
            batch_predictions = ['UNKNOWN'] * len(batch)
        else:
            # Processar resultados
            results_dict = {}
            for result in results:
                if 'request' in result and result['request']:
                    result_id = result['request'].get('id', '')
                    sentiment = result.get('sentiment', 'NEUTRAL')
                    results_dict[result_id] = sentiment.upper()
            
            # Mapear resultados de volta para o batch
            batch_predictions = []
            for idx, (_, row) in enumerate(batch.iterrows()):
                comment_id = f'review_{i + idx}'
                pred_label = results_dict.get(comment_id, 'NEUTRAL')
                batch_predictions.append(pred_label)
        
        predictions.extend(batch_predictions)
        
        if (i + BATCH_SIZE) % 1000 == 0 or (i + BATCH_SIZE) >= len(df):
            elapsed = time.time() - start_time
            rate = (i + BATCH_SIZE) / elapsed if elapsed > 0 else 0
            print(f"   Processado: {min(i + BATCH_SIZE, len(df)):,}/{len(df):,} ({rate:.1f} amostras/seg)")
    
    df['predicted_sentiment'] = predictions
    
    elapsed_time = time.time() - start_time
    print(f"\n✅ Predições obtidas em {elapsed_time:.2f} segundos ({len(df)/elapsed_time:.2f} amostras/seg)")
    print()
    
    # Calcular métricas
    print("📊 Calculando métricas...")
    
    y_true = df['sentiment_label'].tolist()
    y_pred = df['predicted_sentiment'].tolist()
    
    # Determinar labels únicos
    all_labels = sorted(set(y_true + y_pred))
    # Garantir que temos as 3 classes principais
    main_labels = ['NEGATIVE', 'NEUTRAL', 'POSITIVE']
    labels = [l for l in main_labels if l in all_labels] + [l for l in all_labels if l not in main_labels]
    
    metrics = calculate_metrics(y_true, y_pred, labels)
    
    # Exibir resultados
    print("\n" + "=" * 80)
    print("RESULTADOS DA VALIDAÇÃO")
    print("=" * 80)
    print()
    print(f"Dataset: AiresPucrs/sentiment-analysis-pt (Português)")
    print(f"Total de amostras: {len(df):,}")
    print(f"Tempo de processamento: {elapsed_time:.2f} segundos")
    print()
    print("Métricas Gerais:")
    print(f"  Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f"  Precision: {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
    print(f"  Recall:    {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
    print(f"  F1-Score: {metrics['f1_score']:.4f} ({metrics['f1_score']*100:.2f}%)")
    print()
    
    print("Métricas por Classe:")
    print(classification_report(y_true, y_pred, labels=labels, zero_division=0))
    print()
    
    print("Matriz de Confusão:")
    print("                Predicted")
    print(f"              {' '.join([f'{l[:3]:>3}' for l in labels])}")
    for i, true_label in enumerate(labels):
        row = "Actual " + f"{true_label[:3]:>3}" + "  "
        for j, pred_label in enumerate(labels):
            count = metrics['confusion_matrix'][i][j] if i < len(metrics['confusion_matrix']) and j < len(metrics['confusion_matrix'][i]) else 0
            row += f"{count:>4} "
        print(row)
    print()
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"results/validation_airespucrs_pt_{timestamp}.json"
    
    os.makedirs("results", exist_ok=True)
    
    results = {
        'dataset': 'airespucrs_pt',
        'timestamp': timestamp,
        'total_samples': len(df),
        'processing_time_seconds': elapsed_time,
        'metrics': metrics,
        'distribution': df['sentiment_label'].value_counts().to_dict()
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Resultados salvos em: {results_file}")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()

