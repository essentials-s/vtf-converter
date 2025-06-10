import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_png(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    png_path = f"input.png"
    await file.download_to_drive(png_path)

    await update.message.reply_text("⏳ Конвертирую в .vtf...")

    vtf_path = "output.vtf"
    command = f'wine VTFCmd.exe -file "{png_path}" -output "{vtf_path}"'
    process = subprocess.run(command, shell=True)

    if os.path.exists(vtf_path):
        await update.message.reply_document(document=open(vtf_path, "rb"), filename="converted.vtf")
    else:
        await update.message.reply_text("❌ Ошибка при конвертации.")

    os.remove(png_path)
    if os.path.exists(vtf_path):
        os.remove(vtf_path)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.Document.MimeType("image/png"), handle_png))
app.run_polling()
