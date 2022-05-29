from aiogram import types, Dispatcher
from scripts.sql import get_profile
from handlers.fsm import FSM_start
from scripts.excel import get_group_by_fio, get_course_by_fio
from keyboards.kb import menu_markup


async def echo_message(message: types.Message):
    fio = get_profile(message.from_user.id)
    if fio:
        course = get_course_by_fio(fio)
        group = get_group_by_fio(fio)
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \nКурс: {course} \nГруппа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()
    else:
        await message.answer('Вы не зарегистрированы.\nВведите /start чтобы начать')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_message, state="*")
