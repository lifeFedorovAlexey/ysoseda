from telegram import Update
from telegram.ext import CallbackContext

from .config import STOCK, TYPE

async def get_stock(update: Update, context: CallbackContext):
    try:
        context.user_data['stock'] = int(update.message.text)
        await update.message.reply_text("Введите тип продукта:")
        return TYPE
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректное количество.")
        return STOCK