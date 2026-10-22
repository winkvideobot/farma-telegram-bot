import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Bot Token-kaaga
TELEGRAM_TOKEN = "8984653101:AAGrDSKE1sudjxj7rmNklZbJjtQCqRn9FFg"

async def start_and_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Ku soo dhowow Farma AI Create Bot!\n\n"
        "🎬 Noo soo dir link-ga YouTube, aniguna waxaan kuu soo dejinayaa muuqaalkaaga!"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "http://" in text or "https://" in text:
        await update.message.reply_text("⏳ Fadlan sug, waxaan soo dejinayaa muuqaalkaaga...")
        
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': 'downloaded_video.mp4',
                'max_filesize': 50 * 1024 * 1024,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([text])
            
            with open('downloaded_video.mp4', 'rb') as video_file:
                await update.message.reply_video(
                    video=video_file, 
                    caption="✅ Waa kan muuqaalkii aad codsatay!"
                )
                
            if os.path.exists('downloaded_video.mp4'):
                os.remove('downloaded_video.mp4')
                
        except Exception as e:
            await update.message.reply_text(f"❌ Cilad ayaa dhacday: {str(e)}")
    else:
        await update.message.reply_text("Fadlan soo dir link sax ah.")

def main():
    app_tg = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start_and_help))
    app_tg.add_handler(CommandHandler("help", start_and_help))
    app_tg.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Bot-kaagu wuu shaqaynayaa...")
    app_tg.run_polling()

if __name__ == '__main__':
    main()
