from aiogram import types, Dispatcher
from keyboards.kb import menu_markup
from handlers.fsm import FSM_study, FSM_start
from scripts.sql import get_profile
from scripts.excel import get_group_by_fio, get_course_by_fio


async def subjects(message: types.Message):
    if message.text == 'Назад в меню':
        fio = get_profile(message.from_user.id)
        course = get_course_by_fio(fio)
        group = get_group_by_fio(fio)
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \nКурс: {course} \nГруппа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()
    else:
        await message.answer('Пока думаем')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(subjects, state=FSM_study.study)
