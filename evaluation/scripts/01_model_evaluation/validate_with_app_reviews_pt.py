#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validação do Modelo com Dataset de Avaliações de Aplicativos Móveis (Português)

Este script valida o modelo TF-IDF + Logistic Regression usando o dataset
de avaliações de aplicativos móveis da Google Play Store em português brasileiro.

O dataset possui 7 emoções básicas, mas podemos mapear para sentimento (positivo/negativo/neutro).

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

# Configuration
SAMPLE_SIZE = None  # Usar dataset completo se possível, ou balancear
RANDOM_STATE = 42
BATCH_SIZE = 100

# Lambda URL da API de análise de sentimento
SENTIMENT_API_URL = os.environ.get('SENTIMENT_ANALYSIS_API_URL', '')
SENTIMENT_API_KEY = os.environ.get('SENTIMENT_ANALYSIS_API_KEY', '')

# Mapeamento de emoções para sentimento
# O dataset tem 7 emoções, vamos mapear para positivo/negativo/neutro
EMOTION_TO_SENTIMENT = {
    # Emoções positivas
    'alegria': 'POSITIVE',
    'felicidade': 'POSITIVE',
    'satisfação': 'POSITIVE',
    'prazer': 'POSITIVE',
    'joy': 'POSITIVE',
    'happiness': 'POSITIVE',
    'satisfaction': 'POSITIVE',
    'pleasure': 'POSITIVE',
    # Emoções negativas
    'raiva': 'NEGATIVE',
    'tristeza': 'NEGATIVE',
    'desgosto': 'NEGATIVE',
    'medo': 'NEGATIVE',
    'anger': 'NEGATIVE',
    'sadness': 'NEGATIVE',
    'disgust': 'NEGATIVE',
    'fear': 'NEGATIVE',
    # Emoções neutras
    'neutro': 'NEUTRAL',
    'neutral': 'NEUTRAL',
    'surpresa': 'NEUTRAL',  # Pode ser positiva ou negativa, mas vamos considerar neutra
    'surprise': 'NEUTRAL',
}

def load_app_reviews_dataset(file_path=None, sample_size=None):
    """
    Carrega o dataset de avaliações de aplicativos móveis.
    
    Tenta primeiro carregar de um arquivo local, depois tenta baixar de fontes conhecidas.
    """
    print("📊 Carregando dataset de avaliações de aplicativos móveis...")
    
    # Primeiro, tentar carregar de arquivo local se fornecido
    if file_path and os.path.exists(file_path):
        print(f"📂 Carregando de arquivo local: {file_path}")
        df = pd.read_csv(file_path, low_memory=False)
        print(f"✅ Dataset carregado! Shape: {df.shape}")
        print(f"   Colunas: {df.columns.tolist()}")
        return df, None
    
    # Tentar encontrar arquivo na pasta atual ou em subpastas
    import glob
    possible_paths = [
        'data/app_reviews*.csv',
        'data/*app*.csv',
        '*.csv',
        '../data/app_reviews*.csv',
        '../../data/app_reviews*.csv',
    ]
    
    for pattern in possible_paths:
        files = glob.glob(pattern, recursive=True)
        if files:
            file_path = files[0]
            print(f"📂 Arquivo encontrado: {file_path}")
            df = pd.read_csv(file_path, low_memory=False)
            print(f"✅ Dataset carregado! Shape: {df.shape}")
            print(f"   Colunas: {df.columns.tolist()}")
            return df, None
    
    # Se não encontrou arquivo, tentar baixar de fontes conhecidas
    print("⚠️  Arquivo não encontrado localmente.")
    print("📥 Tentando baixar de fontes conhecidas...")
    
    # Tentar URLs conhecidas do dataset
    possible_urls = [
        # Adicionar URLs conhecidas aqui se houver
    ]
    
    for url in possible_urls:
        try:
            print(f"   Tentando: {url}")
            df = pd.read_csv(url)
            print(f"✅ Dataset baixado com sucesso!")
            return df, None
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            continue
    
    # Se não conseguiu baixar, pedir ao usuário
    print("\n❌ Dataset não encontrado automaticamente.")
    print("   Por favor, forneça o caminho para o arquivo CSV do dataset:")
    file_path = input("   Caminho do arquivo: ").strip()
    
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    df = pd.read_csv(file_path, low_memory=False)
    print(f"✅ Dataset carregado! Shape: {df.shape}")
    return df, None

def map_emotions_to_sentiment(df, emotion_col):
    """
    Mapeia as 7 emoções do dataset para sentimento (POSITIVE/NEGATIVE/NEUTRAL).
    """
    print(f"🔄 Mapeando emoções para sentimento...")
    
    # Verificar valores únicos de emoções
    unique_emotions = df[emotion_col].unique()
    print(f"   Emoções encontradas: {unique_emotions}")
    
    # Criar mapeamento
    sentiment_map = {}
    for emotion in unique_emotions:
        emotion_lower = str(emotion).lower().strip()
        
        # Tentar mapear usando o dicionário
        if emotion_lower in EMOTION_TO_SENTIMENT:
            sentiment_map[emotion] = EMOTION_TO_SENTIMENT[emotion_lower]
        else:
            # Heurística: se contém palavras positivas, é positivo; negativas, negativo; senão, neutro
            if any(word in emotion_lower for word in ['alegria', 'felicidade', 'satisfação', 'prazer', 'joy', 'happy', 'satisfaction']):
                sentiment_map[emotion] = 'POSITIVE'
            elif any(word in emotion_lower for word in ['raiva', 'tristeza', 'desgosto', 'medo', 'anger', 'sad', 'disgust', 'fear']):
                sentiment_map[emotion] = 'NEGATIVE'
            else:
                sentiment_map[emotion] = 'NEUTRAL'
    
    print(f"   Mapeamento:")
    for emotion, sentiment in sentiment_map.items():
        print(f"     {emotion} → {sentiment}")
    
    # Aplicar mapeamento
    df['sentiment_label'] = df[emotion_col].map(sentiment_map)
    
    # Verificar distribuição
    print(f"\n📊 Distribuição de sentimentos após mapeamento:")
    print(df['sentiment_label'].value_counts())
    print()
    
    return df

def call_sentiment_api(text):
    """Chama a API de análise de sentimento."""
    if not SENTIMENT_API_URL:
        raise ValueError("SENTIMENT_ANALYSIS_API_URL não configurada")
    
    try:
        response = requests.post(
            SENTIMENT_API_URL,
            json={'text': text},
            headers={
                'x-api-key': SENTIMENT_API_KEY,
                'Content-Type': 'application/json'
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result.get('sentiment', 'UNKNOWN')
    except Exception as e:
        print(f"⚠️  Erro ao chamar API para texto '{text[:50]}...': {e}")
        return 'UNKNOWN'

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
    print("VALIDAÇÃO DO MODELO - AVALIAÇÕES DE APLICATIVOS MÓVEIS (PORTUGUÊS)")
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
        df, text_col = load_app_reviews_dataset(sample_size=SAMPLE_SIZE)
    except Exception as e:
        print(f"❌ Erro ao carregar dataset: {e}")
        print("\n💡 Dica: Se o dataset não estiver disponível, podemos usar o dataset")
        print("   AiresPucrs/sentiment-analysis-pt como alternativa.")
        return
    
    # Identificar colunas
    if text_col is None:
        # Tentar identificar colunas automaticamente
        text_col = None
        emotion_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if 'text' in col_lower or 'coment' in col_lower or 'review' in col_lower or 'avali' in col_lower:
                text_col = col
            if 'emotion' in col_lower or 'emoção' in col_lower or 'sentiment' in col_lower or 'sentimento' in col_lower or 'label' in col_lower:
                emotion_col = col
        
        if text_col is None:
            print("⚠️  Não foi possível identificar coluna de texto automaticamente.")
            print(f"   Colunas disponíveis: {df.columns.tolist()}")
            text_col = input("   Nome da coluna de texto: ").strip()
        
        if emotion_col is None:
            print("⚠️  Não foi possível identificar coluna de emoção automaticamente.")
            print(f"   Colunas disponíveis: {df.columns.tolist()}")
            emotion_col = input("   Nome da coluna de emoção/sentimento: ").strip()
    else:
        # Se text_col foi retornado, precisamos identificar emotion_col
        emotion_col = None
        for col in df.columns:
            col_lower = col.lower()
            if 'emotion' in col_lower or 'emoção' in col_lower or 'sentiment' in col_lower or 'sentimento' in col_lower or 'label' in col_lower:
                emotion_col = col
                break
        
        if emotion_col is None:
            print("⚠️  Não foi possível identificar coluna de emoção automaticamente.")
            print(f"   Colunas disponíveis: {df.columns.tolist()}")
            emotion_col = input("   Nome da coluna de emoção/sentimento: ").strip()
    
    print(f"\n📊 Colunas identificadas:")
    print(f"   Texto: {text_col}")
    print(f"   Emoção: {emotion_col}")
    print()
    
    # Limpar dados
    df = df.dropna(subset=[text_col, emotion_col])
    df = df[df[text_col].notna()].copy()
    df = df[df[text_col].astype(str).str.strip() != ''].copy()
    
    # Mapear emoções para sentimento
    df = map_emotions_to_sentiment(df, emotion_col)
    
    # Balancear se necessário
    sentiment_counts = df['sentiment_label'].value_counts()
    min_class_size = sentiment_counts.min()
    
    if sample_size is not None:
        samples_per_class = min(sample_size // len(sentiment_counts), min_class_size)
    else:
        # Usar dataset completo, mas balancear se houver desbalanceamento significativo
        if sentiment_counts.max() > min_class_size * 1.5:
            samples_per_class = min_class_size
        else:
            samples_per_class = None
    
    if samples_per_class is not None:
        print(f"📊 Balanceando dataset: {samples_per_class} amostras por classe")
        
        sampled_df = pd.DataFrame()
        for label in sentiment_counts.index:
            class_df = df[df['sentiment_label'] == label]
            sampled_df = pd.concat([sampled_df, class_df.sample(n=samples_per_class, random_state=RANDOM_STATE)])
        
        df = sampled_df.reset_index(drop=True)
        df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)  # Shuffle
        
        print(f"   Total balanceado: {len(df)} amostras")
        print(f"📊 Distribuição final:")
        print(df['sentiment_label'].value_counts())
        print()
    
    print(f"📊 Dataset final preparado!")
    print(f"   Total de amostras: {len(df):,}")
    print()
    
    # Obter predições da API
    print("🔄 Obtendo predições da API...")
    print(f"   Processando {len(df):,} amostras em lotes de {BATCH_SIZE}...")
    
    predictions = []
    start_time = time.time()
    
    for i in range(0, len(df), BATCH_SIZE):
        batch = df.iloc[i:i+BATCH_SIZE]
        batch_predictions = []
        
        for idx, row in batch.iterrows():
            text = str(row[text_col])
            sentiment = call_sentiment_api(text)
            batch_predictions.append(sentiment)
        
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
    print(f"Dataset: Avaliações de Aplicativos Móveis (Português)")
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
    results_file = f"results/validation_app_reviews_pt_{timestamp}.json"
    
    os.makedirs("results", exist_ok=True)
    
    results = {
        'dataset': 'app_reviews_pt',
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
