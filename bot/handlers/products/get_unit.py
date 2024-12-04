from telegram import Update
from telegram.ext import CallbackContext

from .config import STOCK

async def get_unit(update: Update, context: CallbackContext):
    context.user_data['unit'] = update.message.text
    await update.message.reply_text("Введите количество на складе:")
    return STOCK