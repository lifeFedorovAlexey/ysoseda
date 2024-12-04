from telegram import Update
from telegram.ext import ContextTypes
from bot.logger import logger
from bot.database import cursor

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name  # Получаем имя пользователя
    
    cursor.execute("SELECT role FROM users WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()

    if user and user[0] == "admin":
        await update.message.reply_text(f"Добро пожаловать, Администратор {first_name}!")
    elif user:
        await update.message.reply_text(f"Добро пожаловать, сосед {first_name}!")
    else:
        await update.message.reply_text(f"Вы незарегистрированный пользователь, {first_name}. Пожалуйста, зарегистрируйтесь с помощью команды /register.")
    
    logger.info(f"Пользователь {first_name} ({user_id}) вызвал команду /start")
