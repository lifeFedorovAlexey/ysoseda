from telegram import Update
from telegram.ext import ContextTypes
from bot.logger import logger
from bot.database import cursor, conn

async def reject_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    first_name = update.effective_user.first_name
    
    # Проверка, что администратор
    cursor.execute("SELECT role FROM users WHERE telegram_id = ?", (admin_id,))
    admin = cursor.fetchone()

    if not admin or admin[0] != 'admin':
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")
        return

    # Получаем user_id для отклонения
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

    # Отклоняем заявку
    if request[0] == 'pending':
        cursor.execute("UPDATE registration_requests SET status = ? WHERE telegram_id = ?", ('rejected', user_id))
        conn.commit()
        
        await update.message.reply_text(f"Заявка пользователя {first_name} была отклонена.")
        await context.bot.send_message(
            chat_id=user_id,
            text="К сожалению, ваша заявка на регистрацию была отклонена."
        )
    else:
        await update.message.reply_text("Эта заявка уже обработана.")
