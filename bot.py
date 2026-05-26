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

    loading = await update.message.reply_text("Downloading video...")

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'format': 'best',
        'quiet': True
        'cookiefile': 'cookies.txt',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        uploader = info.get("uploader", "Unknown")
        title = info.get("title", "No caption")

        caption = f"""
<blockquote>
<b>{uploader}</b>

{title}
</blockquote>

🔗 <a href="{url}">Source</a>
"""

        with open(filename, 'rb') as video:
            await update.message.reply_video(
                video=video,
                caption=caption,
                parse_mode="HTML",
                reply_to_message_id=update.message.message_id
            )

        os.remove(filename)

        await loading.delete()

    except Exception as e:
        await loading.edit_text(f"Error:\n{e}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, download_video)
)

print("Downloader bot is running...")
app.run_polling()