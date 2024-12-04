from telegram import Update
from telegram.ext import ContextTypes
from bot.logger import logger
from bot.database import cursor, conn
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
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

            # Создаем кнопки для разрешения или отклонения регистрации
            keyboard = [
                [
                    InlineKeyboardButton("Разрешить", callback_data=f"approve_{user_id}"),
                    InlineKeyboardButton("Отклонить", callback_data=f"reject_{user_id}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=admin_id,
                text=f"Сосед {first_name} подал заявку на регистрацию. Выберите действие.",
                reply_markup=reply_markup
            )

    logger.info(f"Сосед {first_name} {user_id} подал заявку на регистрацию.")

# Обработка callback-запросов от администраторов
async def button_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = int(query.data.split('_')[1])  # Получаем ID пользователя из callback_data

    if query.data.startswith("approve"):
        # Обновляем статус заявки в базе данных
        cursor.execute("UPDATE registration_requests SET status = ? WHERE telegram_id = ?", ('approved', user_id))
        cursor.execute("INSERT INTO users (telegram_id, role) VALUES (?, ?)", (user_id, 'user'))  # Добавляем пользователя в таблицу users
        conn.commit()

        await query.answer(text="Заявка на регистрацию одобрена.")
        await context.bot.send_message(user_id, "Ваша регистрация одобрена, теперь вы можете использовать бота.")

        # Уведомляем администратора
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"Заявка соседа {first_name} была одобрена."
        )
    elif query.data.startswith("reject"):
        cursor.execute("UPDATE registration_requests SET status = ? WHERE telegram_id = ?", ('rejected', user_id))
        conn.commit()
        
        await query.answer(text="Заявка на регистрацию отклонена.")
        await context.bot.send_message(user_id, "Ваша заявка на регистрацию была отклонена.")

        # Уведомляем администратора
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"Заявка пользователя {user_id} была отклонена."
        )