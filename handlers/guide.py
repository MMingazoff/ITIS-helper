from aiogram import types, Dispatcher
from keyboards.kb import menu_markup, canteens_inline_markup, address_rating_inline_markup, places_inline_markup
from handlers.fsm import FSM_guide, FSM_start
from scripts.sql import get_profile, get_canteen_description, get_canteen_photo, get_canteen_address, \
    get_place_description, get_place_photo, get_place_address, set_points, get_points
from scripts.excel import get_group_by_fio, get_course_by_fio


async def guide(message: types.Message):
    """Меню Гида"""
    if message.text == '\U0001F372 Общепиты':
        catering = 'Вот такие общепиты есть около университета'
        await message.answer(catering, reply_markup=canteens_inline_markup())
    if message.text == '\U0001F919 Места где можно отдохнуть':
        places_to_relax = 'Сюда ты можешь сходить отдохнуть'
        await message.answer(places_to_relax, reply_markup=places_inline_markup())
    if message.text == '\U0001F64F Справочник для первокурсника':
        student_handbook = '<b>Советы от разработчиков бота</b>:\n' \
                           '-заводите друзей в разных группах\n' \
                           '-общайтесь, помогайте друг другу\n' \
                           '-находите друзей в старших группах\n' \
                           '-для простоты сдачи зачетов выбирайте курсы с маркой "в электронной форме"\n' \
                           '-чтобы не вылететь с университета, ходи на физкультуру\n' \
                           '-если ты плохо понимаешь материал, обратись к тьюторам\n' \
                           '-если хочешь закрыть сессию, купи удачу за 100 на паре по психологии'
        await message.answer(student_handbook, parse_mode=types.ParseMode.HTML)
    if message.text == '\U0001F519 Вернуться в меню':
        fio = get_profile(message.from_user.id)
        course = get_course_by_fio(fio)
        group = get_group_by_fio(fio)
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \nКурс: {course} \nГруппа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


async def canteen_info(call: types.CallbackQuery):
    """Информация об общепите"""
    name = call.data[7:]
    description = get_canteen_description(name)
    address = get_canteen_address(name)
    photo = get_canteen_photo(name)
    points = get_points(name.replace(' ', ''))
    await call.bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=f'{name}\n\n{points}\n\n{description}',
                              reply_markup=address_rating_inline_markup(address, name.replace(' ', '')))
    await call.answer()


async def place_info(call: types.CallbackQuery):
    """Информация о месте для отдыха"""
    name = call.data[5:]
    description = get_place_description(name)
    address = get_place_address(name)
    photo = get_place_photo(name)
    points = get_points(name.replace(' ', ''))
    await call.bot.send_photo(chat_id=call.from_user.id, photo=photo, caption=f'{name}\n\n{points}\n\n{description}',
                              reply_markup=address_rating_inline_markup(address, name.replace(' ', '')))
    await call.answer()


async def set_mark(call: types.CallbackQuery):
    """Пользователь ставит оценку"""
    mark = int(call.data[0])
    place = call.data[7:]
    set_points(call.from_user.id, place, mark)
    await call.answer(f'Вы поставили месту оценку: {mark}')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(guide, state=FSM_guide.guide)
    dp.register_callback_query_handler(canteen_info, text_contains='canteen', state='*')
    dp.register_callback_query_handler(place_info, text_contains='place', state='*')
    dp.register_callback_query_handler(set_mark, text_contains='point', state='*')
