from transformers import AutoTokenizer, AutoModelForSequenceClassification
import constants

for model in constants.models:
    model_name = model['name']
    model_path = model['dest_path']
    print(f"Downloading model {model_name}...")
    AutoTokenizer.from_pretrained(model_name).save_pretrained(model_path)
    AutoModelForSequenceClassification.from_pretrained(model_name).save_pretrained(model_path)

# AutoTokenizer.from_pretrained(constants.MODEL_NAME).save_pretrained(constants.DEST_PATH)
# AutoModelForSequenceClassification.from_pretrained(constants.MODEL_NAME).save_pretrained(constants.DEST_PATH)