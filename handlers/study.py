from aiogram import types, Dispatcher
from keyboards import menu_markup
from handlers.fsm import FSM_study, FSM_start


async def subjects(message: types.Message):
    if message.text == 'Назад в меню':
        fio = 'Фамилия Имя Отчество'
        course = 'n-ый'
        group = '***-**'
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \n Курс: {course} \n Группа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()
    else:
        await message.answer('Пока думаем')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(subjects, state=FSM_study.study)
