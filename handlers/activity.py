import aiogram.types
from aiogram import types, Dispatcher
from keyboards import menu_markup, activity_markup, events_inline_markup, someone_points_markup, top_students_markup
from exсel_to_dataframe import df_student
from scripts.vk_parsing import get_posts
from handlers.fsm import FSM_activity, FSM_start


post_num = 0
posts = get_posts("itis_request")


async def activity(message: types.Message):
    if message.text == 'Доступные мероприятия':
        # вывод первого поста
        global post_num
        post_num = 0
        await message.answer(posts[0][0], reply_markup=events_inline_markup(posts[0][1], 0))
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


async def post_navigation(call: types.CallbackQuery):
    global post_num
    if call.data == 'next post':
        post_num += 1
    if call.data == 'prev post':
        post_num -= 1
    await call.message.edit_text(posts[post_num][0], reply_markup=events_inline_markup(posts[post_num][1], post_num))


async def fio_copy_callback(call: types.CallbackQuery):
    # get_profile get_group
    await call.message.answer(f'Нажми на чтобы скопировать:\n`Фамилия Имя Отчество 11-104`',
                              parse_mode=aiogram.types.ParseMode.MARKDOWN)
    await call.answer()


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
    dp.register_callback_query_handler(post_navigation, state=FSM_activity.activity, text_contains='post')
    dp.register_callback_query_handler(fio_copy_callback, state=FSM_activity.activity, text='copy fio')
    dp.register_message_handler(someone_points, state=FSM_activity.someone_points)
    dp.register_message_handler(top_students, state=FSM_activity.top_students)
