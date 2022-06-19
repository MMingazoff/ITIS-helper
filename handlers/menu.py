from aiogram import types, Dispatcher
from keyboards.kb import menu_markup, timetable_markup, study_markup, help_markup, activity_markup, guide_markup, \
    swap_profile_markup
from scripts.excel import get_group_by_fio, get_course_by_fio, is_a_student_by_fio
from scripts.sql import set_profile, get_profile
from handlers.fsm import FSM_start, FSM_study, FSM_guide, FSM_helps, FSM_activity, FSM_timetable


async def start_bot(message: types.Message):
    await message.answer('Привет! Я бот, который поможет тебе в студенческой жизни. Введи свое ФИО')
    await FSM_start.fio.set()


async def enter_fio(message: types.Message):
    fio = message.text
    if is_a_student_by_fio(fio):
        course = get_course_by_fio(fio)
        group = get_group_by_fio(fio)
        set_profile(message.from_user.id, fio)
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \nКурс: {course} \nГруппа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()
    else:
        await message.answer('Такого студента нет, или вы ошиблись c ФИО')
        await FSM_start.fio.set()


async def menu(message: types.Message):
    if message.text == '\U0001F4C5 Расписание':
        fio = get_profile(message.from_user.id)
        course = get_course_by_fio(fio)
        if course == 'аспирантура':
            await message.answer("Извините, но у нас нет расписания аспирантов")
        else:
            await message.answer('Выбери расписание', reply_markup=timetable_markup())
            await FSM_timetable.timetable.set()
    if message.text == '\U0001F4D5 Учеба':
        fio = get_profile(message.from_user.id)
        course = get_course_by_fio(fio)
        if course == 'магистратура':
            await message.answer("Извините, но у нас нет учебных материалов для магистров")
        if course == 'аспирантура':
            await message.answer("Извините, но у нас нет учебных материалов для аспирантов")
        else:
            await message.answer('Выбери нужный тебе предмет', reply_markup=study_markup(course))
            await FSM_study.study.set()
    if message.text == '\U0001F198 Помощь':
        await message.answer('Чем помочь?', reply_markup=help_markup())
        await FSM_helps.help.set()
    if message.text == '\U0001F503 Сменить профиль':
        await FSM_start.swap_profile.set()
        await message.answer('Введи свое ФИО', reply_markup=swap_profile_markup())
    if message.text == '\U000026F3 Активности':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать, где можно заработать баллы\n'
            '<i>Примечание: в рейтинге учитываются баллы реквеста и ДУ</i>',
            reply_markup=activity_markup(),
            parse_mode=types.ParseMode.HTML)
        await FSM_activity.activity.set()
    if message.text == '\U0001F5FA Гид':
        await message.answer('Здесь ты можешь посмотреть места, где можно хорошо провести время',
                             reply_markup=guide_markup())
        await FSM_guide.guide.set()


async def swap_profile(message: types.Message):
    if message.text == '\U0001F519 Вернуться в меню' or is_a_student_by_fio(message.text):
        if message.text == '\U0001F519 Вернуться в меню':
            fio = get_profile(message.from_user.id)
        else:
            fio = message.text
            set_profile(message.from_user.id, fio)
        course = get_course_by_fio(fio)
        group = get_group_by_fio(fio)
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \nКурс: {course} \nГруппа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()
    else:
        await message.answer(f'Возможно вы ошиблись, попробуйте ввести ФИО ещё раз', reply_markup=swap_profile_markup())


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'], state="*")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(enter_fio, state=FSM_start.fio)
    dp.register_message_handler(menu, state=FSM_start.menu)
    dp.register_message_handler(swap_profile, state=FSM_start.swap_profile)
