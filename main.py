import os
import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# Token dari Environment Variables (keamanan Render/Replit)
BOT_A_TOKEN = os.getenv('BOT_A_TOKEN')
BOT_B_TOKEN = os.getenv('BOT_B_TOKEN')

# Hitung balasan per chat_id (anti-loop max 3x)
reply_counter = {}

# Delay slowmode biar lebih natural
async def slow_delay():
    delay = random.uniform(3, 5)
    await asyncio.sleep(delay)

# Command /reset untuk reset counter reply
async def reset_counter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    reply_counter[chat_id] = 0
    await context.bot.send_message(chat_id=chat_id, text="✅ Counter reset. Mulai lagi!")

# Bot A balas user lalu pancing Bot B
async def bot_a_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Kalau dari manusia → reset hitungan awal
    if update.message.from_user.is_bot is False:
        reply_counter[chat_id] = 0

    # Batas max 3 balasan bolak balik
    if reply_counter.get(chat_id, 0) < 3:
        reply_counter[chat_id] += 1
        await context.bot.send_message(chat_id=chat_id, text=f"🤖 Bot A balas #{reply_counter[chat_id]}: Prediksi roulette hari ini bakal seperti apa ya?")

        await slow_delay()

        await bot_b_app.bot.send_message(chat_id=chat_id, text=f"🎯 Bot B balas ke-{reply_counter[chat_id]}: 'jelas dong prediksi disini mantap ga bakal meleset'")

# Bot B balas Bot A lalu pancing balik Bot A
async def bot_b_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Pastikan hanya balas kalau dari Bot A
    if update.message.from_user.id != bot_a_app.bot.id:
        return

    if reply_counter.get(chat_id, 0) < 3:
        reply_counter[chat_id] += 1
        await context.bot.send_message(chat_id=chat_id, text=f"🤖 Bot B balas #{reply_counter[chat_id]}: Prediksi & trick selalu tepat sasaran disini!")

        await slow_delay()

        await bot_a_app.bot.send_message(chat_id=chat_id, text=f"🎯 Bot A balas ke-{reply_counter[chat_id]}: 'bener banget! makanya ga pernah bosen liat tips harian disini'")

# Setup Bot A
bot_a_app = ApplicationBuilder().token(BOT_A_TOKEN).build()
bot_a_app.add_handler(CommandHandler("reset", reset_counter))
bot_a_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), bot_a_reply))

# Setup Bot B
bot_b_app = ApplicationBuilder().token(BOT_B_TOKEN).build()
bot_b_app.add_handler(CommandHandler("reset", reset_counter))
bot_b_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), bot_b_reply))

# Jalankan keduanya paralel polling
async def main():
    await asyncio.gather(
        bot_a_app.run_polling(),
        bot_b_app.run_polling()
    )

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
