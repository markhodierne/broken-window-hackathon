from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from datasets import load_dataset

dataset = load_dataset("huggingface/cats-image")
image = dataset["test"]["image"][0]

image_processor = AutoImageProcessor.from_pretrained("microsoft/resnet-18")
model = AutoModelForImageClassification.from_pretrained("microsoft/resnet-18")

print("READY")
inputs = image_processor(image, return_tensors="pt")
print("INPUTS prepared")

with torch.no_grad():
    logits = model(**inputs).logits
    
print("logits ready")

# model predicts one of the 1000 ImageNet classes
predicted_label = logits.argmax(-1).item()
print("predicted label ready")
print(model.config.id2label[predicted_label])
