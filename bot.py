import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)
import yt_dlp

TOKEN = "8947751365:AAGZ2Hoc05-ZNo9VRxYvXGEj5RGgcjIPFkc"

DOWNLOAD_FOLDER = "downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("Downloading video...")

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'format': 'best'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_text("Uploading video...")

        with open(filename, 'rb') as video:
            await update.message.reply_video(video)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"Error:\n{e}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, download_video)
)

print("Downloader bot is running...")
app.run_polling()