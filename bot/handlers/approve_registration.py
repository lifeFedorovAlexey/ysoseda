from telegram import Update
from telegram.ext import ContextTypes
from bot.logger import logger
from bot.database import cursor, conn

async def approve_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    
    # Проверка, что администратор
    cursor.execute("SELECT role FROM users WHERE telegram_id = ?", (admin_id,))
    admin = cursor.fetchone()

    if not admin or admin[0] != 'admin':
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")
        return

    # Получаем user_id для утверждения
    if len(context.args) != 1:
        await update.message.reply_text("Пожалуйста, укажите user_id заявки.")
        return

    user_id = int(context.args[0])

    # Проверяем, есть ли заявка
    cursor.execute("SELECT status FROM registration_requests WHERE telegram_id = ?", (user_id,))
    request = cursor.fetchone()

    if not request:
        await update.message.reply_text("Заявка с таким user_id не найдена.")
        return

    # Обработка команды
    if request[0] == 'pending':
        # Одобряем заявку
        cursor.execute("UPDATE registration_requests SET status = ? WHERE telegram_id = ?", ('approved', user_id))
        cursor.execute("INSERT INTO users (telegram_id, role) VALUES (?, ?)", (user_id, 'user'))
        conn.commit()
        
        await update.message.reply_text(f"Заявка пользователя {user_id} была одобрена.")
        await context.bot.send_message(
            chat_id=user_id,
            text="Поздравляем, ваша заявка на регистрацию была одобрена. Вы теперь зарегистрированный пользователь!"
        )
    else:
        await update.message.reply_text("Эта заявка уже обработана.")