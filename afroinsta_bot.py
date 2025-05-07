
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Token do bot
TOKEN = "7750861867:AAEyy1h8XbASJGhpvRembHjsiEnJ3oaA65k"

# Ativar logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Mensagens e botões
mensagem_video = "🎬 *Afroinsta Downloader*\n\n✅ Vídeo baixado com sucesso!"
mensagem_pergunta = "🍿 Curte filmes?"

botoes_filmes = InlineKeyboardMarkup([
    [InlineKeyboardButton("📱 Baixar para Android", url="https://links.unitvnet.app/IAFLDMW")],
    [InlineKeyboardButton("🍎 iPhone ou SmartTV", url="https://wa.me/message/3IY74MCWLWN2B1")]
])

# Função principal do bot
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if "instagram.com" in text:
        try:
            api_url = f"https://igram.world/api/instagram?url={text}"
            r = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
            data = r.json()

            if data and "url" in data and len(data["url"]) > 0:
                video_url = data["url"][0]

                await update.message.reply_video(
                    video=video_url,
                    caption=mensagem_video,
                    parse_mode="Markdown"
                )

                await update.message.reply_text(
                    mensagem_pergunta,
                    reply_markup=botoes_filmes
                )
            else:
                await update.message.reply_text("⚠️ Não consegui extrair o vídeo. Tente outro link.")
        except Exception as e:
            await update.message.reply_text("❌ Erro ao processar o vídeo. Tente novamente mais tarde.")
            logging.error(f"Erro: {e}")
    else:
        await update.message.reply_text("Por favor, envie um link válido do Instagram.")

# Mensagem de boas-vindas
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_markdown(
        "👋 *Seja bem-vindo ao Afroinsta Downloader!*\n\n"
        "Me mande um link de Reels ou vídeo do Instagram que eu te envio o conteúdo direto aqui no Telegram.\n\n"
        "🎥 Simples, rápido e sem redirecionamento.\n\n"
        "👇 Experimente agora enviando um link do Instagram!"
    )

# Inicializador do bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
