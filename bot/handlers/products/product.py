from telegram.ext import filters, ConversationHandler, MessageHandler, CommandHandler, CallbackQueryHandler
from . import add_product, get_name, get_price, get_unit, get_stock, get_type, get_image, cancel
from .config import NAME, PRICE, UNIT, STOCK, TYPE, IMAGE

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('add_product', add_product)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
        UNIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_unit)],
        STOCK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_stock)],
        TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_type)],
        IMAGE: [MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, get_image)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)