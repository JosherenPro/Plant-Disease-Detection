import tensorflow as tf
import json
from PIL import Image
import numpy as np

# Chargement des donnees des maladies
with open('json/diseases.json', 'r') as file:
    DISEASES = json.load(file)

# Chargement du model
MODEL_PATH = 'model/'
model = tf.save_model.load(MODEL_PATH)


# Predire la maladie de la plante
def predict_disease(image_path):
    # Charger et petraiter l'image
    img = Image.open(image_path)
    img = img.resize((224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    img = tf.expand_dims(img, axis=0)

    # faire la prediction
    prediction = model(img)
    predicted_class = tf.argmax(prediction, axis=1)
    return predicted_class[0].numpy()


# Trouver la maladie
def find_disease(image_path):
    disease_id = predict_disease(image_path)
    disease_info = DISEASES.get(disease_id, {
        'name': "Maladie Inconnu",
        'solution': "Aucune solution"
    })
    return disease_info['name'], disease_info['solution']
