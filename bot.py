from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

async def translate_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.chat.id == CHANNEL_ID:
        if update.channel_post.text:
            original_text = update.channel_post.text

            # Translate to Spanish
            translated = GoogleTranslator(source='auto', target='es').translate(original_text)

            # Delete original English message
            await context.bot.delete_message(
                chat_id=CHANNEL_ID,
                message_id=update.channel_post.message_id
            )

            # Send Indonesian version
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=translated
            )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, translate_post))

print("Bot is running...")
app.run_polling()
