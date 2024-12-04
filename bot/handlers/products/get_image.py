import os
from telegram import Update
from telegram.ext import CallbackContext
from bot.database import cursor, conn
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

async def get_image(update: Update, context: CallbackContext):
    """Получаем изображение или завершаем процесс."""
    if update.message.photo:
        # Сохраняем изображение (например, файл или URL)
        photo_file = await update.message.photo[-1].get_file()
        photo_path = f"images/{context.user_data['name']}.jpg"
        
        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(photo_path), exist_ok=True)
        
        # Загружаем файл с помощью download_to_drive
        await photo_file.download_to_drive(photo_path)
        context.user_data['image'] = photo_path
    else:
        context.user_data['image'] = None

    # Сохранение в базу данных
    cursor.execute('''INSERT INTO products (name, price, unit, stock, type_id, image)
                  VALUES (?, ?, ?, ?, ?, ?)''',
               (context.user_data['name'], context.user_data['price'], context.user_data['unit'],
                context.user_data['stock'], context.user_data['type'], context.user_data['image']))
    conn.commit()

    await update.message.reply_text("Продукт успешно добавлен!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END