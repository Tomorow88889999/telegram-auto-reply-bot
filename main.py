import os
import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# Ambil token dari Environment Variables (Render Secrets)
BOT_A_TOKEN = os.getenv('BOT_A_TOKEN')
BOT_B_TOKEN = os.getenv('BOT_B_TOKEN')

# Hitungan balasan per chat_id (anti-loop max 3x)
reply_count = {}

# Fungsi delay slowmode biar natural (acak 3-5 detik)
async def slow_delay():
    delay = random.uniform(3, 5)
    await asyncio.sleep(delay)

# Command /reset untuk reset counter reply
async def reset_counter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    reply_count[chat_id] = 0
    await context.bot.send_message(chat_id=chat_id, text="✅ Loop counter direset! Silakan mulai chat lagi.")

# Fungsi balasan Bot A, lalu panggil Bot B
async def bot_a_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = update.message.text

    # Jangan respon kalau user adalah bot
    if update.message.from_user.is_bot is False:
        reply_count[chat_id] = 0

    if reply_count.get(chat_id, 0) < 3:
        reply_count[chat_id] = reply_count.get(chat_id, 0) + 1
        await context.bot.send_message(chat_id=chat_id, text=f"🤖 Bot A balas #{reply_count[chat_id]}: Prediksi roulette hari ini bakal seperti apa ya?")
        await slow_delay()
        await bot_b_app.bot.send_message(chat_id=chat_id, text=f"🎯 Bot B merespon A #{reply_count[chat_id]}: 'ya sudah jelas pasti nya bakal tembus terus ga mungkin meleset'")

# Fungsi balasan Bot B, lalu panggil Bot A lagi
async def bot_b_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = update.message.text

    if reply_count.get(chat_id, 0) < 3:
        reply_count[chat_id] = reply_count.get(chat_id, 0) + 1
        await context.bot.send_message(chat_id=chat_id, text=f"🤖 Bot B balas #{reply_count[chat_id]}: Emang paling mantap tuh disini prediksi dan trick selalu tepat sasaran")
        await slow_delay()
        await bot_a_app.bot.send_message(chat_id=chat_id, text=f"🎯 Bot A merespon B #{reply_count[chat_id]}: 'ya jelas dong makanya ga pernah bosen mantengin tips and trick setiap hari nya dsni'")

# Setup Bot A
bot_a_app = ApplicationBuilder().token(BOT_A_TOKEN).build()
bot_a_app.add_handler(CommandHandler("reset", reset_counter))
bot_a_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), bot_a_reply))

# Setup Bot B
bot_b_app = ApplicationBuilder().token(BOT_B_TOKEN).build()
bot_b_app.add_handler(CommandHandler("reset", reset_counter))
bot_b_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), bot_b_reply))

# Jalankan 2 bot secara paralel
async def main():
    await asyncio.gather(
        bot_a_app.run_polling(),
        bot_b_app.run_polling()
    )

if __name__ == '__main__':
    asyncio.run(main())
