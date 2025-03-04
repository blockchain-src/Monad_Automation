import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from src.utils.config import Config


async def send_telegram_message(config: Config, message: str) -> None:
    """使用来自配置的机器人令牌向 Telegram 用户发送消息。"""
    bot = Bot(token=config.SETTINGS.TELEGRAM_BOT_TOKEN)

    for user_id in config.SETTINGS.TELEGRAM_USERS_IDS:
        await bot.send_message(chat_id=user_id, text=message, parse_mode=ParseMode.HTML)
        await asyncio.sleep(1)
        
    await bot.session.close()
