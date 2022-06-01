from aiogram import types, Dispatcher
from keyboards.kb import menu_markup
from handlers.fsm import FSM_guide, FSM_start
from scripts.sql import get_profile
from scripts.excel import get_group_by_fio, get_course_by_fio


async def guide(message: types.Message):
    if message.text == 'Общепиты':
        catering = 'Тут должны быть общепиты'
        await message.answer(catering)
    if message.text == 'Места где можно отдохнуть':
        places_to_relax = 'Тут должны быть места для отдыха'
        await message.answer(places_to_relax)
    if message.text == 'Справочник для первокурсника':
        student_handbook = 'Тут будет что-то связанное с помощью студенту'
        await message.answer(student_handbook)
    if message.text == 'Вернуться в меню':
        fio = get_profile(message.from_user.id)
        course = get_course_by_fio(fio)
        group = get_group_by_fio(fio)
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \nКурс: {course} \nГруппа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(guide, state=FSM_guide.guide)
