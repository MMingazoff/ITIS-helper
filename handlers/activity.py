import aiogram.types
from aiogram import types, Dispatcher
from keyboards.kb import (menu_markup,
                          activity_markup,
                          events_inline_markup,
                          someone_points_markup,
                          top_students_markup,
                          delete_msg_inline_markup,
                          choose_events_markup)
from scripts.excel import is_a_student_by_fi
from scripts.vk_parsing import get_request_posts, get_du_posts
from handlers.fsm import FSM_activity, FSM_start
from scripts.sql import get_profile
from scripts.excel import get_group_by_fio, get_course_by_fio, from_du, get_fio_by_fi
from scripts.activity import sorted_balls, get_students_balls_place
from time import strftime


request_posts = list()
du_posts = list()
rating = sorted_balls()
students = get_students_balls_place(rating)


def update_activity():
    global rating, students
    rating = sorted_balls()
    students = get_students_balls_place(rating)
    print(f'{strftime("%d-%m-%Y %H:%M:%S")}: balls updated successfully')


async def activity(message: types.Message):
    if message.text == '\U0000267F Доступные мероприятия':
        fio = get_profile(message.from_user.id)
        if from_du(fio):
            await message.answer("Какие мероприятия тебе нужны?", reply_markup=choose_events_markup())
            await FSM_activity.activities.set()
        else:
            setattr(activity, 'throttling_rate_limit', 0.5)
            # вывод первого поста
            global request_posts
            request_posts = get_request_posts()
            await message.answer(request_posts[0][0],
                                 reply_markup=events_inline_markup("itisrequest", request_posts[0][1], 0),
                                 parse_mode=types.ParseMode.HTML,
                                 disable_web_page_preview=True)
    if message.text == '\U0001F4C9 Узнать свое место в рейтинге':
        fio = get_profile(message.from_user.id)
        balls, place = students[fio]
        await message.answer(f"Ты на {place} месте в топе\nУ тебя {balls} баллов")
    if message.text == '\U0001F575 Узнать баллы человека':
        await message.answer('Введите фамилию и имя человека', reply_markup=someone_points_markup())
        await FSM_activity.someone_points.set()
    if message.text == '\U0001F51D Общий рейтинг':
        await message.answer('Выберите нужную вам часть топа', reply_markup=top_students_markup())
        await FSM_activity.top_students.set()
    if message.text == '\U0001F519 Вернуться в меню':
        fio = get_profile(message.from_user.id)
        course = get_course_by_fio(fio)
        group = get_group_by_fio(fio)
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \nКурс: {course} \nГруппа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


async def choose_activity(message: types.Message):
    setattr(choose_activity, 'throttling_rate_limit', 0.5)
    if message.text == 'ITIS Request':
        global request_posts
        request_posts = get_request_posts()
        await message.answer(request_posts[0][0],
                             reply_markup=events_inline_markup("itisrequest", request_posts[0][1], 0),
                             parse_mode=types.ParseMode.HTML,
                             disable_web_page_preview=True)
    if message.text == 'ДУ 18':
        global du_posts
        du_posts = get_du_posts()
        await message.answer(du_posts[0][0],
                             reply_markup=events_inline_markup("du", du_posts[0][1], 0),
                             parse_mode=types.ParseMode.HTML,
                             disable_web_page_preview=True)
    if message.text == '\U0001F519 Вернуться в активность':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать где можно заработать баллы',
            reply_markup=activity_markup())
        await FSM_activity.activity.set()


async def post_navigation(call: types.CallbackQuery):
    group_name, post_num = call.data.split('post')
    group_name = group_name[:-4]
    post_num = int(post_num)
    if 'next' in call.data:
        post_num += 1
    if 'prev' in call.data:
        post_num -= 1
    if group_name == 'itisrequest':
        global request_posts
        await call.message.edit_text(request_posts[post_num][0],
                                     reply_markup=events_inline_markup("itisrequest",
                                                                       request_posts[post_num][1],
                                                                       post_num),
                                     parse_mode=types.ParseMode.HTML,
                                     disable_web_page_preview=True)
    if group_name == 'du':
        global du_posts
        await call.message.edit_text(du_posts[post_num][0],
                                     reply_markup=events_inline_markup("du", du_posts[post_num][1], post_num),
                                     parse_mode=types.ParseMode.HTML,
                                     disable_web_page_preview=True)

    await call.answer()


async def fio_copy_callback(call: types.CallbackQuery):
    fio = get_profile(call.from_user.id)
    group = '\b'
    if call.data.endswith('group'):
        group = get_group_by_fio(fio)
    await call.message.answer(f'Нажми, чтобы скопировать 👇:\n`{fio} {group}`',
                              parse_mode=aiogram.types.ParseMode.MARKDOWN,
                              reply_markup=delete_msg_inline_markup())
    await call.answer()


async def delete_msg_callback(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer()


async def someone_points(message: types.Message):
    if is_a_student_by_fi(message.text):
        fio = get_fio_by_fi(message.text)
        balls, place = students[fio]
        await message.answer(f"{message.text} на {place} месте в топе\nУ него/неё {balls} баллов",
                             reply_markup=activity_markup())
        await FSM_activity.activity.set()
    elif message.text == '\U0001F519 Вернуться в активность':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать где можно заработать баллы',
            reply_markup=activity_markup())
        await FSM_activity.activity.set()
    else:
        await message.answer('Такого человека нету, введите фамилию и имя ещё раз')


async def top_students(message: types.Message):
    if message.text == '1-10 место':
        rating_out = '\n'.join(f"{place}. {' '.join(fio.split()[:2])}, {balls} баллов" for place, (fio, balls) in rating[:10])
        await message.answer(rating_out)
    if message.text == '11-20 место':
        rating_out = '\n'.join(f"{place}. {' '.join(fio.split()[:2])}, {balls} баллов" for place, (fio, balls) in rating[10:20])
        await message.answer(rating_out)
    if message.text == '21-30 место':
        rating_out = '\n'.join(f"{place}. {' '.join(fio.split()[:2])}, {balls} баллов" for place, (fio, balls) in rating[20:30])
        await message.answer(rating_out)
    if message.text == '\U0001F519 Вернуться в активность':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать где можно заработать баллы',
            reply_markup=activity_markup())
        await FSM_activity.activity.set()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(activity, state=FSM_activity.activity)
    dp.register_message_handler(choose_activity, state=FSM_activity.activities)
    dp.register_callback_query_handler(post_navigation, state="*", text_contains='post')
    dp.register_callback_query_handler(fio_copy_callback, state="*", text_contains='copyfio')
    dp.register_callback_query_handler(delete_msg_callback, state="*", text='todelete')
    dp.register_message_handler(someone_points, state=FSM_activity.someone_points)
    dp.register_message_handler(top_students, state=FSM_activity.top_students)
