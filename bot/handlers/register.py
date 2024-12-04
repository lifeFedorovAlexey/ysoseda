from telegram import Update
from telegram.ext import ContextTypes
from bot.logger import logger
from bot.database import cursor, conn

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        await update.message.reply_text("Вы уже зарегистрированы!")
    else:
        cursor.execute("INSERT INTO users (telegram_id, role) VALUES (?, ?)", (user_id, 'user'))
        conn.commit()
        await update.message.reply_text("Вы успешно зарегистрированы!")
    logger.info(f"Пользователь {user_id} зарегистрировался")
