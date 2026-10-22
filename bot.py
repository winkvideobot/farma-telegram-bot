import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

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
        "👋 Ku soo dhowow Farma AI Create Bot!\n"
        "Sidee baan ku caawinnaa maanta?"
    )

# Qabashada fariimaha caadiga ah adigoo aan lahayn culeys soo-dejin
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
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
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot-kii waa uu bilowday oo waa uu shaqaynayaa...")
    application.run_polling()
