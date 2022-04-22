from aiogram import types, Dispatcher
from keyboards import menu_markup, activity_markup, events_markup, someone_points_markup, top_students_markup
from exсel_to_dataframe import df_student
from handlers.fsm import FSM_activity, FSM_start


async def activity(message: types.Message):
    if message.text == 'Доступные мероприятия':
        await message.answer('Тут будет список свободных мероприятий', reply_markup=events_markup())
        await FSM_activity.events.set()
    if message.text == 'Я в рейтинге':
        ur_place = 'Тут будут твое место и твои баллы'
        await message.answer(ur_place)
    if message.text == 'Узнать баллы человека':
        await message.answer('Введите фамилию и имя человека', reply_markup=someone_points_markup())
        await FSM_activity.someone_points.set()
    if message.text == 'Общий рейтинг':
        await message.answer('Тут должен быть список студнтов с 1 по 10 место', reply_markup=top_students_markup())
        await FSM_activity.top_students.set()
    if message.text == 'Вернуться в меню':
        fio = 'Фамилия Имя Отчество'
        course = 'n-ый'
        group = '***-**'
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \n Курс: {course} \n Группа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


async def events(message: types.Message):
    if message.text == 'Скопировать ФИО и группу':
        await message.answer('Копируешь свое фио')
    if message.text == 'Назад в активность':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать где можно заработать баллы',
            reply_markup=activity_markup())
        await FSM_activity.activity.set()


async def someone_points(message: types.Message):
    if any(df_student.ФИО == message.text):
        await message.answer(f'У {message.text} n баллов и он на k месте')
    elif message.text == 'Назад в активность':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать где можно заработать баллы',
            reply_markup=activity_markup())
        await FSM_activity.activity.set()
    else:
        await message.answer('Такого человека нету, введите фамилию и имя ещё раз')


async def top_students(message: types.Message):
    if message.text == '1-10 место':
        rating = 'Тут должен быть список студнтов с 1 по 10 место'
        await message.answer(rating)
    if message.text == '11-20 место':
        rating = 'Тут должен быть список студнтов с 11 по 20 место'
        await message.answer(rating)
    if message.text == '21-30 место':
        rating = 'Тут должен быть список студнтов с 21 по 30 место'
        await message.answer(rating)
    if message.text == 'Назад в активность':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать где можно заработать баллы',
            reply_markup=activity_markup())
        await FSM_activity.activity.set()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(activity, state=FSM_activity.activity)
    dp.register_message_handler(events, state=FSM_activity.events)
    dp.register_message_handler(someone_points, state=FSM_activity.someone_points)
    dp.register_message_handler(top_students, state=FSM_activity.top_students)
