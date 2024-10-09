import os
from dotenv import load_dotenv
import tensorflow_hub as hub
import tensorflow as tf
from tensorflow.keras.models import load_model
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image
import numpy as np
import kagglehub

# Le token de notre bot Telegram
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Charger le modèle depuis Kaggle
path = kagglehub.model_download("rishitdagli/plant-disease/tensorFlow2/plant-disease")
model = load_model(path)  # Charge le modèle


# Fonction pour prédire la maladie de la plante
def predict_disease(image_path):
    # Charger et prétraiter l'image
    img = Image.open(image_path)
    img = img.resize((224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    img = tf.expand_dims(img, axis=0)

    # Faire la prédiction
    prediction = model(img)
    predicted_class = tf.argmax(prediction, axis=1)
    return predicted_class[0].numpy()


# Fonction pour trouver la maladie
def find_disease(image_path):
    res = predict_disease(image_path)
    diseases = {
        "0": "Apple___Apple_scab",
        "1": "Apple___Black_rot",
        "2": "Apple___Cedar_apple_rust",
        "3": "Apple___healthy",
        "4": "Blueberry___healthy",
        "5": "Cherry_(including_sour)___Powdery_mildew",
        "6": "Cherry_(including_sour)___healthy",
        "7": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "8": "Corn_(maize)___Common_rust_",
        "9": "Corn_(maize)___Northern_Leaf_Blight",
        "10": "Corn_(maize)___healthy",
        "11": "Grape___Black_rot",
        "12": "Grape___Esca_(Black_Measles)",
        "13": "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        "14": "Grape___healthy",
        "15": "Orange___Haunglongbing_(Citrus_greening)",
        "16": "Peach___Bacterial_spot",
        "17": "Peach___healthy",
        "18": "Pepper_bell___Bacterial_spot",
        "19": "Pepper_bell___healthy",
        "20": "Potato___Early_blight",
        "21": "Potato___Late_blight",
        "22": "Potato___healthy",
        "23": "Raspberry___healthy",
        "24": "Soybean___healthy",
        "25": "Squash___Powdery_mildew",
        "26": "Strawberry___Leaf_scorch",
        "27": "Strawberry___healthy",
        "28": "Tomato___Bacterial_spot",
        "29": "Tomato___Early_blight",
        "30": "Tomato___Late_blight",
        "31": "Tomato___Leaf_Mold",
        "32": "Tomato___Septoria_leaf_spot",
        "33": "Tomato___Spider_mites Two-spotted_spider_mite",
        "34": "Tomato___Target_Spot",
        "35": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "36": "Tomato___Tomato_mosaic_virus",
        "37": "Tomato___healthy"
    }
    return diseases[str(res)]


# Fonction de "start" dans le bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Envoyez-moi une image de feuille de la plante pour détecter la maladie.")


# Fonction de gestion des images
def handle_photo(update: Update, context: CallbackContext) -> None:
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('image/temp_photo.jpg')  # Télécharger l'image

    disease_name = find_disease('image/temp_photo.jpg')  # Prédire la maladie
    update.message.reply_text(f"La maladie détectée est : {disease_name}")


# La fonction principale pour démarrer le bot
def main() -> None:
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
