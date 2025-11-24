#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validação do Modelo com Dataset IMDB Movie Reviews

Este script valida o modelo TF-IDF + Logistic Regression usando o dataset
IMDB Movie Reviews como validação independente. Este dataset geralmente possui
2 classes (positive/negative), mas pode ser adaptado para incluir neutral.

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
import kagglehub

# Configuration
SAMPLE_SIZE = 10000  # Usando 10k reviews para validação
RANDOM_STATE = 42
BATCH_SIZE = 100

# Lambda URL da API de análise de sentimento
SENTIMENT_API_URL = os.environ.get('SENTIMENT_ANALYSIS_API_URL', '')
SENTIMENT_API_KEY = os.environ.get('SENTIMENT_ANALYSIS_API_KEY', '')

# Sentiment mapping - IMDB geralmente tem apenas positive/negative
IMDB_MAP = {
    'positive': 'POSITIVE',
    'negative': 'NEGATIVE',
    'pos': 'POSITIVE',
    'neg': 'NEGATIVE',
    1: 'POSITIVE',
    0: 'NEGATIVE'
}

def load_imdb_dataset(file_path=None, sample_size=None):
    """
    Carrega o dataset IMDB Movie Reviews.
    
    Tenta baixar automaticamente do Kaggle usando kagglehub.
    """
    print("📊 Carregando dataset IMDB Movie Reviews...")
    
    if file_path is None:
        try:
            print("📥 Tentando baixar dataset do Kaggle...")
            # Tentar diferentes nomes comuns do dataset IMDB
            possible_datasets = [
                "lakshmi25npathi/imdb-dataset-of-50k-movie-reviews",
                "utathya/imdb-review-dataset",
                "imdb-movie-reviews"
            ]
            
            path = None
            for dataset_name in possible_datasets:
                try:
                    path = kagglehub.dataset_download(dataset_name)
                    print(f"✅ Dataset baixado: {dataset_name}")
                    break
                except:
                    continue
            
            if path is None:
                raise FileNotFoundError("Dataset IMDB não encontrado no Kaggle")
            
            # Procurar arquivo CSV
            import glob
            csv_files = glob.glob(f'{path}/**/*.csv', recursive=True)
            if csv_files:
                file_path = csv_files[0]
            else:
                # Listar arquivos disponíveis
                print(f"📂 Conteúdo do diretório: {os.listdir(path)}")
                for file in os.listdir(path):
                    if file.endswith('.csv'):
                        file_path = os.path.join(path, file)
                        break
                
                if not file_path:
                    raise FileNotFoundError("Arquivo CSV não encontrado")
                    
        except Exception as e:
            print(f"⚠️  Erro ao baixar do Kaggle: {e}")
            raise FileNotFoundError(
                "Dataset não encontrado. Baixe manualmente de:\n"
                "https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews"
            )
    
    print(f"📂 Carregando de: {file_path}")
    
    # Carregar CSV
    try:
        df = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
    except:
        df = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
    
    print(f"✅ Dataset carregado! Shape: {df.shape}")
    print(f"   Colunas: {df.columns.tolist()}")
    
    # Identificar colunas
    text_col = None
    sentiment_col = None
    
    for col in df.columns:
        col_lower = col.lower()
        if 'review' in col_lower or 'text' in col_lower or 'comment' in col_lower:
            text_col = col
        if 'sentiment' in col_lower or 'label' in col_lower:
            sentiment_col = col
    
    if text_col is None or sentiment_col is None:
        print("⚠️  Colunas não identificadas. Primeiras linhas:")
        print(df.head())
        raise ValueError("Não foi possível identificar colunas de texto e sentimento")
    
    print(f"   Coluna de texto: {text_col}")
    print(f"   Coluna de sentimento: {sentiment_col}")
    
    # Filtrar apenas sentimentos válidos
    unique_sentiments = df[sentiment_col].unique()
    print(f"   Sentimentos únicos encontrados: {unique_sentiments}")
    
    # Mapear sentimentos
    df['sentiment_label'] = df[sentiment_col].map(IMDB_MAP)
    
    # Filtrar apenas os que foram mapeados
    df = df[df['sentiment_label'].notna()].copy()
    
    # Remover linhas com texto vazio
    df = df[df[text_col].notna()].copy()
    df = df[df[text_col].astype(str).str.strip() != ''].copy()
    
    print(f"✅ Após filtragem: {df.shape}")
    
    # Verificar distribuição original
    print("📈 Distribuição original de sentimentos:")
    original_dist = df['sentiment_label'].value_counts()
    print(original_dist)
    print()
    
    # Amostrar com estratificação
    if sample_size and sample_size < len(df):
        print(f"📊 Amostrando {sample_size:,} reviews com estratificação por classe...")
        samples_per_class = sample_size // len(original_dist)
        print(f"   Amostras por classe: {samples_per_class:,}")
        
        sampled_dfs = []
        for sentiment in original_dist.index:
            class_df = df[df['sentiment_label'] == sentiment]
            if len(class_df) >= samples_per_class:
                sampled_class = class_df.sample(n=samples_per_class, random_state=RANDOM_STATE)
            else:
                print(f"   ⚠️  Classe {sentiment} tem apenas {len(class_df)} amostras")
                sampled_class = class_df
            sampled_dfs.append(sampled_class)
        
        df = pd.concat(sampled_dfs, ignore_index=True)
        df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
        
        if len(df) > sample_size:
            df = df.head(sample_size)
    
    print("📈 Distribuição final de sentimentos (após amostragem):")
    print(df['sentiment_label'].value_counts())
    print()
    
    return df, text_col

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

def validate_batch(reviews_batch, text_col, api_url, api_key=None):
    """Valida um lote de reviews usando a API."""
    comments = []
    for idx, (_, row) in enumerate(reviews_batch.iterrows()):
        comments.append({
            'id': f'review_{idx}',
            'text': str(row[text_col]),
            'videoTitle': None
        })
    
    results, error = call_sentiment_api(comments, api_url, api_key)
    
    if results is None:
        print(f"    ⚠️  Erro na API: {error}")
        return [], []
    
    results_dict = {}
    for result in results:
        if 'request' in result and result['request']:
            result_id = result['request'].get('id', '')
            sentiment = result.get('sentiment', 'NEUTRAL')
            results_dict[result_id] = sentiment.upper()
    
    y_true = []
    y_pred = []
    
    for idx, (_, row) in enumerate(reviews_batch.iterrows()):
        comment_id = f'review_{idx}'
        true_label = row['sentiment_label']
        pred_label = results_dict.get(comment_id, 'NEUTRAL')
        
        y_true.append(true_label)
        y_pred.append(pred_label)
    
    return y_true, y_pred

def calculate_metrics(y_true, y_pred):
    """Calcula métricas de classificação."""
    labels = sorted(list(set(y_true + y_pred)))
    
    if len(labels) == 0:
        return {
            'accuracy': 0.0,
            'precision': 0.0,
            'recall': 0.0,
            'f1_score': 0.0,
            'confusion_matrix': None,
            'total_samples': 0
        }
    
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm,
        'confusion_matrix_labels': labels,
        'total_samples': len(y_true)
    }

def main():
    """Função principal."""
    print("="*80)
    print("VALIDAÇÃO DO MODELO COM DATASET IMDB MOVIE REVIEWS")
    print("="*80)
    print()
    print("Objetivo: Validar generalização do modelo em dataset independente")
    print("Dataset: IMDB Movie Reviews - Reviews de filmes (geralmente 2 classes)")
    print("Modelo: TF-IDF + Logistic Regression (treinado em YouTube comments)")
    print()
    print(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Carregar dataset
    try:
        df, text_col = load_imdb_dataset(sample_size=SAMPLE_SIZE)
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # Verificar API
    global SENTIMENT_API_URL, SENTIMENT_API_KEY
    
    if not SENTIMENT_API_URL:
        print("❌ URL da API não configurada!")
        return
    
    print(f"🔗 API URL: {SENTIMENT_API_URL}")
    if SENTIMENT_API_KEY:
        print(f"🔑 API Key: {'*' * len(SENTIMENT_API_KEY)}")
    print()
    
    # Processar em lotes
    print(f"\n🔄 Processando {len(df):,} reviews em lotes de {BATCH_SIZE}...")
    print()
    
    all_y_true = []
    all_y_pred = []
    
    total_batches = (len(df) + BATCH_SIZE - 1) // BATCH_SIZE
    start_time = time.time()
    
    for i in range(0, len(df), BATCH_SIZE):
        batch_num = (i // BATCH_SIZE) + 1
        batch = df.iloc[i:i+BATCH_SIZE]
        
        print(f"  [{batch_num:4d}/{total_batches}] Processando lote ({len(batch)} reviews)...", end=" ", flush=True)
        
        y_true_batch, y_pred_batch = validate_batch(batch, text_col, SENTIMENT_API_URL, SENTIMENT_API_KEY)
        
        if len(y_true_batch) == 0:
            print("⚠️  Lote falhou - pulando...", flush=True)
            continue
        
        all_y_true.extend(y_true_batch)
        all_y_pred.extend(y_pred_batch)
        
        elapsed = time.time() - start_time
        rate = len(all_y_true) / elapsed if elapsed > 0 else 0
        progress_pct = (batch_num / total_batches) * 100
        remaining_batches = total_batches - batch_num
        eta_seconds = (remaining_batches * elapsed / batch_num) if batch_num > 0 else 0
        eta_minutes = eta_seconds / 60
        
        print(f"✓ ({rate:.1f} reviews/s) | {progress_pct:.1f}% | ETA: {eta_minutes:.1f}min", flush=True)
    
    processing_time = time.time() - start_time
    
    print()
    print(f"✅ Processamento concluído!")
    print(f"   Tempo total: {processing_time:.2f}s")
    print(f"   Taxa: {len(all_y_true)/processing_time:.1f} reviews/s")
    print()
    
    # Calcular métricas
    print("📊 Calculando métricas...")
    from collections import Counter
    true_dist = Counter(all_y_true)
    print("📊 Distribuição no ground truth:")
    for label, count in sorted(true_dist.items()):
        print(f"   {label}: {count:,} ({count/len(all_y_true)*100:.1f}%)")
    print()
    
    metrics = calculate_metrics(all_y_true, all_y_pred)
    
    # Exibir resultados
    print()
    print("="*80)
    print("RESULTADOS DA VALIDAÇÃO")
    print("="*80)
    print()
    print(f"Total de reviews validadas: {metrics['total_samples']:,}")
    print()
    print("Métricas:")
    print(f"  Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f"  Precision: {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
    print(f"  Recall:    {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
    print(f"  F1-Score: {metrics['f1_score']:.4f} ({metrics['f1_score']*100:.2f}%)")
    print()
    
    # Matriz de confusão
    cm = metrics['confusion_matrix']
    cm_labels = metrics.get('confusion_matrix_labels', [])
    
    print("Matriz de Confusão:")
    print("                Predicted")
    header = "              " + "  ".join([label[:3] for label in cm_labels])
    print(header)
    
    for i, true_label in enumerate(cm_labels):
        row_label = f"Actual {true_label[:3]:3s}"
        row_values = " ".join([f"{cm[i, j]:6d}" for j in range(len(cm_labels))])
        print(f"{row_label:12s} {row_values}")
    print()
    
    # Relatório detalhado
    print("Relatório de Classificação:")
    labels_for_report = sorted(list(set(all_y_true + all_y_pred)))
    report = classification_report(all_y_true, all_y_pred, labels=labels_for_report, zero_division=0)
    print(report)
    
    # Salvar resultados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f'results/validation_imdb_{timestamp}.json'
    os.makedirs('results', exist_ok=True)
    
    results_data = {
        'dataset': 'IMDB Movie Reviews',
        'language': 'English',
        'model': 'TF-IDF + Logistic Regression',
        'api_url': SENTIMENT_API_URL,
        'total_samples': metrics['total_samples'],
        'processing_time_seconds': processing_time,
        'reviews_per_second': len(all_y_true) / processing_time if processing_time > 0 else 0,
        'metrics': {
            'accuracy': float(metrics['accuracy']),
            'precision': float(metrics['precision']),
            'recall': float(metrics['recall']),
            'f1_score': float(metrics['f1_score'])
        },
        'confusion_matrix': cm.tolist() if cm is not None else None,
        'confusion_matrix_labels': metrics.get('confusion_matrix_labels', []),
        'timestamp': timestamp
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Resultados salvos em: {results_file}")
    print()
    print("="*80)
    print("VALIDAÇÃO CONCLUÍDA")
    print("="*80)

if __name__ == "__main__":
    main()

