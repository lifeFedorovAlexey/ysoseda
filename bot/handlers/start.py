from telegram import Update
from telegram.ext import ContextTypes
from bot.logger import logger
from bot.database import cursor

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cursor.execute("SELECT role FROM users WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()

    if user and user[0] == "admin":
        await update.message.reply_text("Добро пожаловать, Администратор!")
    elif user:
        await update.message.reply_text("Добро пожаловать, зарегистрированный пользователь!")
    else:
        await update.message.reply_text("Вы незарегистрированный пользователь. Пожалуйста, зарегистрируйтесь с помощью команды /register.")
    logger.info(f"Пользователь {user_id} вызвал команду /start")
