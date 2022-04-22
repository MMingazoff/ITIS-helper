from aiogram import Dispatcher
from handlers import menu
from handlers import timetable
from handlers import activity
from handlers import study
from handlers import guide
from handlers import help


def register_handlers(dp: Dispatcher):
    menu.register_handlers(dp)
    timetable.register_handlers(dp)
    activity.register_handlers(dp)
    study.register_handlers(dp)
    guide.register_handlers(dp)
    help.register_handlers(dp)
