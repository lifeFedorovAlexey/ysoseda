from telegram import Update
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Добавление продукта отменено.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END