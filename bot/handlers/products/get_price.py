from telegram import Update
from telegram.ext import CallbackContext

from .config import PRICE, UNIT

async def get_price(update: Update, context: CallbackContext):
    try:
        context.user_data['price'] = float(update.message.text)
        await update.message.reply_text("Введите единицу измерения (например, кг, литры, штуки):")
        return UNIT
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректную цену.")
        return PRICE