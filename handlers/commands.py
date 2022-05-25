from aiogram import Dispatcher
from handlers import menu
from handlers import admin


def register_commands(dp: Dispatcher):
    menu.register_commands(dp)
    admin.register_commands(dp)
