from aiogram import types, Dispatcher
from keyboards import menu_markup, timetable_markup, study_markup, help_markup, activity_markup, guide_markup
from scripts import *
from handlers.fsm import FSM_start, FSM_study, FSM_guide, FSM_helps, FSM_activity, FSM_timetable
from exсel_to_dataframe import df_student


async def start_bot(message: types.Message):
    await message.answer('Привет! Я бот, который поможет тебе в студенческой жизни. Введи свое ФИО')
    await FSM_start.fio.set()


async def enter_fio(message: types.Message):
    fio = message.text
    if any(df_student.ФИО == fio):
        course = 'n-ый'
        group = '***-**'
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \n Курс: {course} \n Группа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()
    else:
        await message.answer('Такого студента нету, или вы ошиблись c ФИО')
        await FSM_start.fio.set()


async def menu(message: types.Message):
    if message.text == 'Расписание':
        await message.answer('Выбери расписание', reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()
    if message.text == 'Учеба':
        course = get_course('student_name')
        await message.answer('Выбери нужный тебе предмет', reply_markup=study_markup(course))
        await FSM_study.study.set()
    if message.text == 'Помощь':
        await message.answer('Чем помочь?', reply_markup=help_markup())
        await FSM_helps.help.set()
    if message.text == 'Сменить профиль':
        await FSM_start.fio.set()
        await message.answer('Введи свое ФИО')
    if message.text == 'Активности':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать где можно заработать баллы',
            reply_markup=activity_markup())
        await FSM_activity.activity.set()
    if message.text == 'Гид':
        await message.answer('Здесь ты можешь посмотреть места, где можно хорошо провести время',
                             reply_markup=guide_markup())
        await FSM_guide.guide.set()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'], state="*")
    dp.register_message_handler(enter_fio, state=FSM_start.fio)
    dp.register_message_handler(menu, state=FSM_start.menu)
