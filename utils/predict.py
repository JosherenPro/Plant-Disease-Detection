import tensorflow as tf
import json
from PIL import Image
import numpy as np
import tensorflow_hub as hub

# Chargement des donnees des maladies
with open('./json/disease.json', 'r', encoding='utf-8') as file:
    DISEASES = json.load(file)

# Download and load the latest version of the model

model = hub.load("https://kaggle.com/models/rishitdagli/plant-disease/frameworks/TensorFlow2/variations/plant-disease/versions/1")


if model:
    print("Modèle chargé avec succès")
else:
    print("Échec du chargement du modèle")


# Prédire la maladie de la plante
def predict_disease(image_path):
    try:
        # Charger et prétraiter l'image
        # Load the image and preprocess it
        img = Image.open('./'+image_path)
        print(img)
        img = img.resize((224, 224))
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
        img = tf.expand_dims(img, axis=0)

        # Make the prediction
        prediction = model(img)
        predicted_class = tf.argmax(prediction, axis=1)
        
        print(predicted_class)
        return int(predicted_class)

    except Exception as e:
        print(f"Erreur lors de la prédiction : {e}")
        return None

# Trouver la maladie
def find_disease(image_path):
    disease_info = {'name': "Maladie Inconnue", 'solution': "Aucune solution"}
    disease_id = predict_disease(image_path)

    if disease_id is not None:
        disease_info = DISEASES.get(str(disease_id), disease_info)

    return disease_info['name'], disease_info['solution']
