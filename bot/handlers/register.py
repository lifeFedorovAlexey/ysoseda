from telegram import Update
from telegram.ext import ContextTypes
from bot.logger import logger
from bot.database import cursor, conn

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()

    # Если пользователь уже зарегистрирован
    if user:
        await update.message.reply_text("Вы уже зарегистрированы!")
        return

    # Проверяем, есть ли заявка
    cursor.execute("SELECT status FROM registration_requests WHERE telegram_id = ?", (user_id,))
    request = cursor.fetchone()

    if request:
        if request[0] == 'pending':
            await update.message.reply_text("Ожидайте подтверждения вашей регистрации.")
        else:
            await update.message.reply_text("Ваша заявка на регистрацию была отклонена.")
    else:
        # Добавляем заявку на регистрацию
        cursor.execute("INSERT INTO registration_requests (telegram_id, status) VALUES (?, ?)", (user_id, 'pending'))
        conn.commit()
        await update.message.reply_text("Ваша заявка на регистрацию отправлена. Ожидайте подтверждения.")

        # Отправляем уведомление администратору
        cursor.execute("SELECT telegram_id FROM users WHERE role = 'admin'")
        admins = cursor.fetchall()
        for admin in admins:
            admin_id = admin[0]
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"Пользователь с ID {user_id} подал заявку на регистрацию. Ожидайте решения."
            )
    
    logger.info(f"Пользователь {user_id} подал заявку на регистрацию.")
