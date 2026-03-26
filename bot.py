from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

import os

BOT_TOKEN = "8744657534:AAHeAodObOvm8QtRee1PFGPFfXBzTY7-3Yk"
CHANNEL_ID = -1003833506135

async def translate_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.chat.id == CHANNEL_ID:
        # Get text from either plain text or caption
        original_text = update.channel_post.text or update.channel_post.caption

        if original_text:
            # Translate to Spanish
            translated = GoogleTranslator(source='auto', target='es').translate(original_text)

            # Delete original message
            await context.bot.delete_message(
                chat_id=CHANNEL_ID,
                message_id=update.channel_post.message_id
            )

            # Send translated message
            if update.channel_post.photo:
                # If it was a photo, resend photo with translated caption
                await context.bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=update.channel_post.photo[-1].file_id,  # highest resolution
                    caption=translated
                )
            elif update.channel_post.document:
                # If it was a document, resend document with translated caption
                await context.bot.send_document(
                    chat_id=CHANNEL_ID,
                    document=update.channel_post.document.file_id,
                    caption=translated
                )
            else:
                # Otherwise, just send text
                await context.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=translated
                )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, translate_post))

print("Bot is running...")
app.run_polling()