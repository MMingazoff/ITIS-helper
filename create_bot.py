import asyncio
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middleware import ThrottlingMiddleware

loop = asyncio.get_event_loop()
storage = MemoryStorage()
bot = Bot(token=TOKEN, loop=loop)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(ThrottlingMiddleware())
