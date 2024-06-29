from transformers import CLIPProcessor, CLIPModel
import requests
import torch
import os
from PIL import Image

image_directory = 'images'

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)

inputs = processor(text=["a photo of a cat", "a photo of a dog"], images=image, return_tensors="pt", padding=True)

outputs = model(**inputs)
logits_per_image = outputs.logits_per_image # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities


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

