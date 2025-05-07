import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Envie um link de vídeo do Instagram e eu trago o download!")

def baixar_video_instagram(insta_url):
    try:
        snapinsta_url = "https://snapinsta.io/api/ajaxSearch"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://snapinsta.io",
            "Referer": "https://snapinsta.io/",
            "User-Agent": "Mozilla/5.0"
        }
        data = {
            "q": insta_url,
            "t": "media",
            "lang": "en"
        }
        response = requests.post(snapinsta_url, headers=headers, data=data)
        if '"url":"' in response.text:
            video_link = response.text.split('"url":"')[1].split('"')[0].replace('\\', '')
            return video_link
        return None
    except Exception as e:
        logging.error(f"Erro ao baixar: {e}")
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    insta_url = update.message.text.strip()
    if "instagram.com" not in insta_url:
        await update.message.reply_text("Me manda um link válido do Instagram.")
        return

    await update.message.reply_text("Baixando o vídeo, segura aí...")

    video_url = baixar_video_instagram(insta_url)

    if video_url:
        await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url)

        keyboard = [
            [InlineKeyboardButton("Android (Baixar App)", url="https://links.unitvnet.app/IAFLDMW")],
            [InlineKeyboardButton("iPhone / Smart TV", url="https://wa.me/message/3IY74MCWLWN2B1")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🎬 Curte filmes? A gente tem o app perfeito pra você!",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("Não consegui baixar esse vídeo. Tenta outro link ou aguarda um pouco.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
