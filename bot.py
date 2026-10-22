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

# Command-ka Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Ku soo dhowow Farma AI Create Bot!\n\n"
        "📥 Noo soo dir link-ga YouTube ama TikTok, aniguna waxaan kuu soo dejinayaa muqaalkaaga!"
    )

# Qabashada Link-yada uu soo diro isticmaalaha
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "http://" in text or "https://" in text:
        await update.message.reply_text("⏳ Fadlan sug, waxaan soo dejinayaa muqaalkaaga...")
        
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(id)s.%(ext)s',
                'max_filesize': 50 * 1024 * 1024, # Xaddid 50MB si uusan u culeys badnaan
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                filename = ydl.prepare_filename(info)
            
            # U dir muqaalka isticmaalaha
            await update.message.reply_video(video=open(filename, 'rb'))
            
            # Ka tirtir faylka kombuyuutarka markuu diro
            if os.path.exists(filename):
                os.remove(filename)
                
        except Exception as e:
            logging.error(f"Khalad ayaa dhacay: {e}")
            await update.message.reply_text("❌ Waan ka xumahay, ma awoodin inaan soo dejiyo muqaalkan. Fadlan hubi link-ga.")
    else:
        await update.message.reply_text("Fadlan noo soo dir link sax ah (oo leh http ama https).")

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
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    
    print("Bot-kii waa uu bilowday oo waa uu shaqaynayaa...")
    application.run_polling()
