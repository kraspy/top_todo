import os
from dotenv import load_dotenv
from asgiref.sync import async_to_sync

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def send_message_sync(message):
    async def send_message():
        from aiogram import Bot, exceptions

        bot = Bot(token=API_TOKEN)  # type: ignore
        try:
            await bot.send_message(chat_id=CHAT_ID, text=message)  # type: ignore
        except exceptions.TelegramAPIError as e:
            print(f"Ошибка при отправке сообщения: {e}")
        finally:
            await bot.session.close()

    async_to_sync(send_message)()
