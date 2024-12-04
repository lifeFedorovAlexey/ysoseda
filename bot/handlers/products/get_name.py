from telegram import Update
from telegram.ext import CallbackContext

from .config import PRICE

async def get_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Введите цену продукта:")
    return PRICE