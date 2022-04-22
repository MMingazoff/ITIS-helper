from aiogram import types, Dispatcher
from keyboards import menu_markup, today_tomorrow_markup, timetable_markup, timetable_someone_markup
from scripts import *
from handlers.fsm import FSM_timetable, FSM_start
from exсel_to_dataframe import df_student, list_group


async def timetable(message: types.Message):
    if message.text == 'Расписание на неделю':
        text = get_week_timetable(str(message.from_user))
        await message.answer(text)
    if message.text == 'Расписание на день':
        await message.answer('Выбери нужный день', reply_markup=today_tomorrow_markup())
        await FSM_timetable.today_tomorrow.set()
    if message.text == 'Какая у меня сейчас пара':
        text = get_now_lesson(str(message.from_user))
        await message.answer(text)
    if message.text == 'Узнать пары у другого человека':
        await message.answer('Введи номер группы или фамилию с именем', reply_markup=timetable_someone_markup())
        await FSM_timetable.someone_timetable.set()

    if message.text == 'Назад в меню':
        fio = 'Фамилия Имя Отчество'
        course = 'n-ый'
        group = '***-**'
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \n Курс: {course} \n Группа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


async def timetable_day_lessons(message: types.Message):
    if message.text == 'Пары сегодня':
        text = get_today_lessons(str(message.from_user))
        await message.answer(text)
    if message.text == 'Пары завтра':
        text = get_tomorrow_lessons(str(message.from_user))
        await message.answer(text)
    if message.text == 'Вернуться в расписание':
        await message.answer('Выбери расписание', reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()


async def timetable_someone(message: types.Message):
    if any(df_student.ФИО == message.text):
        text = get_today_lessons(str(message.from_user))
        await message.answer(text, reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()
    elif message.text in list_group:
        text = get_today_lessons_by_group(message.text)
        await message.answer(text, reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()
    elif message.text == 'Вернуться в расписание':
        await message.answer('Выбери расписание', reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()

    else:
        await message.answer('Такого ученика/группы нету, попробуйте ввести заново')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(timetable, state=FSM_timetable.timetable)
    dp.register_message_handler(timetable_day_lessons, state=FSM_timetable.today_tomorrow)
    dp.register_message_handler(timetable_someone, state=FSM_timetable.someone_timetable)



