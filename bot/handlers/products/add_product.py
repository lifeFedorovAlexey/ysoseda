from telegram import Update
from telegram.ext import CallbackContext

from .config import NAME

async def add_product(update, context):
    await update.message.reply_text("Введите название продукта:")
    return NAME