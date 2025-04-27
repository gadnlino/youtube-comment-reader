from transformers import pipeline

# Modelos
model_a = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
model_b = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")

# Comentários
comments = [
    "Esse vídeo é incrível, aprendi demais!",
    "Não gostei, conteúdo fraco e mal explicado.",
    "Legalzinho até, mas faltaram detalhes importantes.",
    "Kkkkkk que vergonha alheia",
    "Ótimo conteúdo, parabéns pelo trabalho!",
    "Essa explicação é ruim demais, perdeu meu tempo.",
    "Achei interessante."
]

# Resultado
print("Comparativo de Sentimento:\n")

for comment in comments:
    result_a = model_a(comment)[0]
    result_b = model_b(comment)[0]

    print(f"Comentário: {comment}")
    print(f"  Modelo A (nlptown) => {result_a['label']} (score {result_a['score']:.2f})")
    print(f"  Modelo B (cardiffnlp) => {result_b['label']} (score {result_b['score']:.2f})")
    print("-" * 60)