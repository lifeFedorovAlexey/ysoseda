from telegram import Update
from telegram.ext import CallbackContext

from .config import IMAGE

async def get_type(update: Update, context: CallbackContext):
    context.user_data['type'] = update.message.text
    await update.message.reply_text("Прикрепите изображение продукта (или напишите 'Пропустить'):")
    return IMAGE