from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
dest = "./models/bert-multilingual"

AutoTokenizer.from_pretrained(model_name).save_pretrained(dest)
AutoModelForSequenceClassification.from_pretrained(model_name).save_pretrained(dest)