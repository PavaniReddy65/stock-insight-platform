import os
from django.core.management.base import BaseCommand
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from api.models import Prediction
from django.contrib.auth.models import User

BOT_TOKEN = os.getenv('BOT_TOKEN')

class Command(BaseCommand):
    help = "Run Telegram Bot"

    def handle(self, *args, **options):
        if not BOT_TOKEN:
            self.stdout.write(self.style.ERROR("BOT_TOKEN not set"))
            return

        bot = Bot(token=BOT_TOKEN)
        updater = Updater(bot=bot, use_context=True)

        def start(update: Update, context: CallbackContext):
            update.message.reply_text("Welcome to Stock Insight Bot!")

        def predict(update: Update, context: CallbackContext):
            user = User.objects.first()  # Simplification, map telegram chat_id to User in production
            if len(context.args) != 1:
                update.message.reply_text("Usage: /predict <TICKER>")
                return
            ticker = context.args[0].upper()
            # You should trigger the prediction logic here; simplified for demo
            update.message.reply_text(f"Prediction for {ticker} is being processed...")

        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(CommandHandler('predict', predict))

        updater.start_polling()
        updater.idle()
