from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
import os
from PIL import Image

image_directory = 'images'

image_processor = AutoImageProcessor.from_pretrained("microsoft/resnet-18")
model = AutoModelForImageClassification.from_pretrained("microsoft/resnet-18")

def classify_images(image_directory):
    results = []
    for filename in os.listdir(image_directory):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(image_directory, filename)
            image = Image.open(image_path).convert("RGB")
            inputs = image_processor(image, return_tensors="pt")
            with torch.no_grad():
                logits = model(**inputs).logits
            predicted_label = logits.argmax(-1).item()
            label = model.config.id2label[predicted_label]
            results.append((filename, label))

    return results

results = classify_images(image_directory)
for filename, label in results:
    print(f"{filename}: {label}")

