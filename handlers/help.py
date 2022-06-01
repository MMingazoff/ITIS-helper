import os
from create_bot import bot
from aiogram import types, Dispatcher
from keyboards.kb import menu_markup, help_markup, wishes_markup
from handlers.fsm import FSM_helps, FSM_start
from scripts.sql import get_profile, get_everything, get_elders
from scripts.excel import get_group_by_fio, get_course_by_fio, get_all_group_members


async def help(message: types.Message):
    if message.text == 'Список моей группы':
        fio = get_profile(message.from_user.id)
        group = get_group_by_fio(fio)
        # Для фото списка группы (пока нам не нужно)
        # photo_path = os.path.abspath(__file__)[:-16] + f'data/groups/{group}.png'
        # if os.path.exists(photo_path):
        #     with open(photo_path, 'rb') as photo:
        #         await bot.send_photo(chat_id=message.chat.id, photo=photo)
        # else:
        #     await message.answer('Извините, у нас нет фото списка вашей группы')
        group_list = group + '\n' + '\n'.join(f'{num}. {fio}' for num, fio in enumerate(get_all_group_members(group), 1))
        await message.answer(group_list)
    if message.text == 'Полезные ссылки':
        links = '\n'.join(f'{name}: {link}' for name, link in get_everything('links'))
        await message.answer(links)
    if message.text == 'Список старост':
        elders = '\n'.join(f'{group}: {fi} {contact}' for group, fi, contact in get_elders())
        await message.answer(elders)
    if message.text == 'Ваши пожелания для бота':
        await message.answer('Введите ваши пожелания', reply_markup=wishes_markup())
        await FSM_helps.wishes.set()
    if message.text == 'Вернуться в меню':
        fio = get_profile(message.from_user.id)
        course = get_course_by_fio(fio)
        group = get_group_by_fio(fio)
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \nКурс: {course} \nГруппа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


async def wishes(message: types.Message):
    if message.text == 'Вернуться в помощь':
        await message.answer('Чем помочь?', reply_markup=help_markup())
        await FSM_helps.help.set()
    else:
        await message.answer(f'Мы рассмотрим вашу идею', reply_markup=help_markup())
        await bot.send_message(text=f'{message.from_user.mention}\n{message.text}', chat_id=-1001603217169)  # группа с ботом
        await FSM_helps.help.set()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(help, state=FSM_helps.help)
    dp.register_message_handler(wishes, state=FSM_helps.wishes)
