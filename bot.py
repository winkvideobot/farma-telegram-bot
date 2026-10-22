import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Web Server yar oo Render u sheegaya inuu port-ka furan yahay
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Farma AI Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Telegram Bot Command-yada
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Ku soo dhowow Farma AI Create Bot!\n"
        "📥 Noo soo dir link-ga YouTube, aniguna waxaan kuu soo dejinayaa muqaalkaaga!"
    )

if __name__ == '__main__':
    # Bilow Web Server-ka dhinaca arka
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    # Token-ka ka akhriso Render Environment
    TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        raise ValueError("Fadlan geli TOKEN ama BOT_TOKEN gudaha Environment Variables!")

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("Bot-kii waa uu bilowday oo waa uu shaqaynayaa...")
    application.run_polling()
