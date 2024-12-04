import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import filters  
from bot.logger import logger
from bot.database import cursor, conn
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardRemove

# Состояния
NAME, PRICE, UNIT, STOCK, TYPE, IMAGE = range(6)

async def add_product(update, context):
    await update.message.reply_text("Введите название продукта:")
    return NAME

# Переработанные функции
async def get_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Введите цену продукта:")
    return PRICE

async def get_price(update: Update, context: CallbackContext):
    try:
        context.user_data['price'] = float(update.message.text)
        await update.message.reply_text("Введите единицу измерения (например, кг, литры, штуки):")
        return UNIT
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректную цену.")
        return PRICE

async def get_unit(update: Update, context: CallbackContext):
    context.user_data['unit'] = update.message.text
    await update.message.reply_text("Введите количество на складе:")
    return STOCK

async def get_stock(update: Update, context: CallbackContext):
    try:
        context.user_data['stock'] = int(update.message.text)
        await update.message.reply_text("Введите тип продукта:")
        return TYPE
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректное количество.")
        return STOCK

async def get_type(update: Update, context: CallbackContext):
    context.user_data['type'] = update.message.text
    await update.message.reply_text("Прикрепите изображение продукта (или напишите 'Пропустить'):")
    return IMAGE

async def get_image(update: Update, context: CallbackContext):
    """Получаем изображение или завершаем процесс."""
    if update.message.photo:
        # Сохраняем изображение (например, файл или URL)
        photo_file = await update.message.photo[-1].get_file()  # добавляем await
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


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Добавление продукта отменено.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Обработчик беседы
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('add_product', add_product)],
    states={
        NAME: [MessageHandler(filters.ALL & ~filters.COMMAND, get_name)],
        PRICE: [MessageHandler(filters.ALL & ~filters.COMMAND, get_price)],
        UNIT: [MessageHandler(filters.ALL & ~filters.COMMAND, get_unit)],
        STOCK: [MessageHandler(filters.ALL & ~filters.COMMAND, get_stock)],
        TYPE: [MessageHandler(filters.ALL & ~filters.COMMAND, get_type)],
        IMAGE: [MessageHandler(filters.ALL | filters.PHOTO & ~filters.COMMAND, get_image)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)