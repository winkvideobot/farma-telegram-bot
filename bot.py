import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Web Server yar si Render uusan u xirin
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Farma AI Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Amarada Start iyo Help
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Ku soo dhowow Farma AI Create Bot!\n\n"
        "📥 Noo soo dir link-ga YouTube ama TikTok, aniguna waxaan kuu soo dejinayaa muqaalkaaga!\n"
        "Isku day amarrada:\n"
        "/dadka - Macluumaadka dadka\n"
        "/help - Caawinaad"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Sida loo isticmaalo bot-ka:\n"
        "Kaliya soo dir link sax ah oo YouTube ama TikTok ah, bot-ku wuu kuu soo dejin doonaa."
    )

async def dadka_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👥 Boggan waxaa maamula Farma AI Create, waa bot kuu diyaariyay adeegyada muqaallada.")

# Qabashada fariimaha iyo link-yada
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "http://" in text or "https://" in text:
        await update.message.reply_text("⏳ Fadlan sug, waxaan soo dejinayaa muqaalkaaga...")
        
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(id)s.%(ext)s',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                filename = ydl.prepare_filename(info)
            
            await update.message.reply_video(video=open(filename, 'rb'))
            
            if os.path.exists(filename):
                os.remove(filename)
                
        except Exception as e:
            logging.error(f"Khalad: {e}")
            await update.message.reply_text("❌ Waan ka xumahay, ma awoodin inaan soo dejiyo muqaalkan. Fadlan hubi link-ga.")
    else:
        await update.message.reply_text(f"Fariintaadii waa la helay: {text}")

if __name__ == '__main__':
    # Bilow Web Server-ka dhinaca arka
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    # Token-ka Bot-ka
    TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        raise ValueError("Fadlan geli TOKEN ama BOT_TOKEN gudaha Environment Variables!")

    application = ApplicationBuilder().token(TOKEN).build()
    
    # Ku darista amarrada oo dhan
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dadka", dadka_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    
    print("Bot-kii waa uu bilowday oo waa uu shaqaynayaa...")
    application.run_polling()
