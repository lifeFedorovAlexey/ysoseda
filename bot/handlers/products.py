from telegram import Update
from telegram.ext import ContextTypes
from bot.logger import logger
from bot.database import cursor, conn

async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Реализация добавления товара
    pass

async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Реализация списка товаров
    pass
