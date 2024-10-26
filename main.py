import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from utils.predict import find_disease  # Assuming this function takes the image path

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Envoyez-moi une image de feuille de la plante pour détecter la maladie.")

# Handle incoming photos
async def handle_photo(update: Update, context: CallbackContext) -> None:
    try:
        file_id = update.message.photo[-1].file_id
        new_file = await context.bot.get_file(file_id)
        
        # Define the path to save the image
        image_path = 'image/temp_image.jpg'
        
        # Download the image
        await new_file.download_to_drive(image_path)

        # Predict the disease
        disease_name = find_disease(image_path)
        maladie = disease_name[0]
        solution = disease_name[1]
        ligne = '--' * 4
        #await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
        await update.message.reply_text(f"La maladie détectée sur votre plante 🌿  est : {maladie}\n{ligne}\nConseil 🔧 :{solution}")
        

    except Exception as e:
        await update.message.reply_text("Une erreur est survenue lors de la prédiction de la maladie. Veuillez réessayer.")
        print(f"Erreur lors du traitement de l'image : {e}")

# Main function to start the bot
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("Bot is running...")
    
    application.run_polling()

if __name__ == '__main__':
    main()
