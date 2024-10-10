import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from utils.predict import find_disease, predict_disease

# Le token de notre bot Telegram
load_dotenv()
TOKEN = os.getenv('TOKEN')


# Fonction de "start" dans le bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Envoyez-moi une image de feuille de la plante pour détecter la maladie.")


# Fonction de gestion des images
def handle_photo(update: Update, context: CallbackContext) -> None:
    try:
        photo_file = update.message.photo[-1].get_file()
        image_path = 'image/temp_image.jpg'
        photo_file.download(image_path)  # Télécharger l'image

        # Prédire la maladie
        disease_name = find_disease(image_path)
        update.message.reply_text(f"La maladie détectée est : {disease_name}")

    except Exception as e:
        update.message.reply_text("Une erreur est survenue lors de la prédiction de la maladie. Veuillez réessayer.")
        print(f"Erreur lors du traitement de l'image : {e}")


# La fonction principale pour démarrer le bot
def main() -> None:
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
