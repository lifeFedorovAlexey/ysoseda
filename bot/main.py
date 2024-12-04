import sys
from telegram.ext import Application
from telegram.ext import CommandHandler
from bot.handlers.start import start
from bot.handlers.register import register
from bot.handlers.products import add_product, list_products
from bot.handlers.orders import make_order, list_orders, process_order
from bot.database import init_db
from bot.logger import logger
from config import BOT_TOKEN

# Для Windows устанавливаем ProactorEventLoop
if sys.platform == "win32":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def main():
    """Основная функция для запуска бота"""
    # Инициализация базы данных
    init_db()

    # Создание экземпляра приложения
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("add_product", add_product))
    application.add_handler(CommandHandler("list_products", list_products))
    application.add_handler(CommandHandler("make_order", make_order))
    application.add_handler(CommandHandler("list_orders", list_orders))
    application.add_handler(CommandHandler("process_order", process_order))

    # Логируем запуск бота
    logger.info("Бот запущен!")

    # Запуск polling
    application.run_polling()

if __name__ == "__main__":
    main()