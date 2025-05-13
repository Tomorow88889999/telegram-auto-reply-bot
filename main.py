import os
import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_A_TOKEN = os.getenv(7780406598 AAHiV8VpDiez_dVOSEbJMePMxq4t1gjibEo)
BOT_B_TOKEN = os.getenv(7593884250 AAHsJ_1N6N2rymJdsP6s_Dx3lRjFmd50kW8)

# Hitungan balasan per chat_id
reply_count = {3}

# Delay slowmode (acak 3-5 detik biar natural)
async def slow_delay():
    delay = random.uniform(3, 5)
    await asyncio.sleep(delay)

# Perintah /reset untuk reset hitungan
async def reset_counter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    reply_count[chat_id] = 0
    await context.bot.send_message(chat_id=chat_id, text="✅ Loop counter direset! Silakan mulai chat lagi.")

# Bot A balas lalu panggil Bot B (maks 3x + delay slowmode)
async def bot_a_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = update.message.text

    if update.message.from_user.is_bot is False:
        reply_count[chat_id] = 0

    if reply_count.get(chat_id, 0) < 3:
        reply_count[chat_id] = reply_count.get(chat_id, 0) + 1
        await context.bot.send_message(chat_id=chat_id, text=f"🤖 Bot A balas #{reply_count[chat_id]}: {message}")
        await slow_delay()
        await bot_b_app.bot.send_message(chat_id=chat_id, text=f"🎯 Bot B merespon A #{reply_count[chat_id]}: '{message}'")

# Bot B balas lalu panggil Bot A lagi (maks 3x + delay slowmode)
async def bot_b_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = update.message.text

    if reply_count.get(chat_id, 0) < 3:
        reply_count[chat_id] = reply_count.get(chat_id, 0) + 1
        await context.bot.send_message(chat_id=chat_id, text=f"🤖 Bot B balas #{reply_count[chat_id]}: {message}")
        await slow_delay()
        await bot_a_app.bot.send_message(chat_id=chat_id, text=f"🎯 Bot A merespon B #{reply_count[chat_id]}: '{message}'")

# Setup Bot A
bot_a_app = ApplicationBuilder().token(BOT_A_TOKEN).build()
bot_a_app.add_handler(CommandHandler("reset", reset_counter))
bot_a_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), bot_a_reply))

# Setup Bot B
bot_b_app = ApplicationBuilder().token(BOT_B_TOKEN).build()
bot_b_app.add_handler(CommandHandler("reset", reset_counter))
bot_b_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), bot_b_reply))

async def main():
    await asyncio.gather(bot_a_app.initialize(), bot_b_app.initialize())
    await asyncio.gather(bot_a_app.start(), bot_b_app.start())
    await asyncio.gather(bot_a_app.updater.start_polling(), bot_b_app.updater.start_polling())

asyncio.run(main())
