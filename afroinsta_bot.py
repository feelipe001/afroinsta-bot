
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Token do bot
TOKEN = "7750861867:AAEyy1h8XbASJGhpvRembHjsiEnJ3oaA65k"

# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Função principal do bot
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "instagram.com" in text:
        response_text = (
            "🎬 *Afroinsta Downloader*\n\n"
            "🔗 Aqui está seu link de download:\n"
            f"[Clique aqui para baixar o vídeo](https://afroinsta.online/afroinsta_download.php?url={text})\n\n"
            "📲 Curte filmes? Baixe nosso app parceiro: [Clique aqui](https://links.unitvnet.app/IAFLDMW)"
        )
        await update.message.reply_markdown(response_text)
    else:
        await update.message.reply_text("Por favor, envie um link válido do Instagram.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salve! Me mande um link do Instagram que eu te mando o download 🎬")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
