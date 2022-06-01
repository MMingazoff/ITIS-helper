from aiogram import types, Dispatcher
from keyboards.admin_kb import main_markup, interact_markup
from handlers.fsm import FSM_admin, FSM_cafes, FSM_elders, FSM_useful_links, FSM_leisure_places
from scripts.sql import add_elder, del_elder, add_link, del_link


async def admin_start(message: types.Message):
    await message.answer("Выбери нужную категорию", reply_markup=main_markup())
    await FSM_admin.is_admin.set()


async def edit_section(message: types.Message):
    next_answer = True
    if message.text == "\U0001F517 Полезные ссылки":
        await FSM_admin.useful_links.set()
    elif message.text == "\U0001F474 Список старост":
        await FSM_admin.elders.set()
    elif message.text == "\U0001F372 Общепиты":
        await FSM_admin.cafes.set()
    elif message.text == "\U0001F919 Места где можно отдохнуть":
        await FSM_admin.leisure_places.set()
    else:
        await message.answer("Используй клавиатуру")
        next_answer = False
    if next_answer:
        await message.answer("Выбери нужное", reply_markup=interact_markup())


async def edit_links(message: types.Message):
    if message.text == "Добавить":
        await message.answer("Введи название сслыки и саму ссылку через ;\n(название ; ссылка)")
        await FSM_useful_links.to_add.set()
    if message.text == "Удалить":
        await message.answer("Введи название сслыки которую хочешь удалить")
        await FSM_useful_links.to_delete.set()


async def edit_elders(message: types.Message):
    if message.text == "Добавить":
        await message.answer("Введи фамилию и имя старосты и контакты старосты через ;\n(ФИ ; контакты)")
        await FSM_elders.to_add.set()
    if message.text == "Удалить":
        await message.answer("Введи фамилию и имя старосты которого хочешь удалить")
        await FSM_elders.to_delete.set()


async def edit_cafes(message: types.Message):
    if message.text == "Добавить":
        await message.answer("не продумано")
        await FSM_cafes.to_add.set()
    if message.text == "Удалить":
        await message.answer("не продумано")
        await FSM_cafes.to_delete.set()


async def edit_places(message: types.Message):
    if message.text == "Добавить":
        await message.answer("не продумано")
        await FSM_leisure_places.to_add.set()
    if message.text == "Удалить":
        await message.answer("не продумано")
        await FSM_leisure_places.to_delete.set()


async def add_elder_handler(message: types.Message):
    try:
        fi, contact = message.text.split(';')
        if add_elder(fi.strip(), contact.strip()):
            await message.answer("Добавление старосты прошло успешно")
            await FSM_admin.elders.set()
        else:
            await message.answer("Такого студента нет, либо староста уже есть в списке")
    except ValueError:
        await message.answer("Ошибочка, попробуй еще раз")


async def del_elder_handler(message: types.Message):
    if del_elder(message.text):
        await message.answer("Староста удален")
        await FSM_admin.elders.set()
    else:
        await message.answer("Староста не найден :(")


async def add_link_handler(message: types.Message):
    try:
        name, link = message.text.split(';')
        if add_link(name.strip(), link.strip()):
            await message.answer("Добавление ссылки прошло успешно")
            await FSM_admin.useful_links.set()
        else:
            await message.answer("Ссылка уже есть в списке")
    except ValueError:
        await message.answer("Ошибочка, попробуй еще раз")


async def del_link_handler(message: types.Message):
    if del_link(message.text):
        await message.answer("Ссылка удалена")
        await FSM_admin.useful_links.set()
    else:
        await message.answer("Такой ссылки нет")


async def add_place_handler(message: types.Message):
    await message.answer("не сделано")


async def del_place_handler(message: types.Message):
    await message.answer("не сделано")


async def add_cafe_handler(message: types.Message):
    await message.answer("не сделано")


async def del_cafe_handler(message: types.Message):
    await message.answer("не сделано")


def register_commands(dp: Dispatcher):
    dp.register_message_handler(admin_start, state='*', commands=['admin', 'cancel'], is_chat_admin=True, chat_id=-1001603217169)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(edit_section, state=FSM_admin.is_admin)
    # регистрация каждой секции
    dp.register_message_handler(edit_links, state=FSM_admin.useful_links)
    dp.register_message_handler(edit_cafes, state=FSM_admin.cafes)
    dp.register_message_handler(edit_places, state=FSM_admin.leisure_places)
    dp.register_message_handler(edit_elders, state=FSM_admin.elders)
    # добавление/удаление каждой секции
    dp.register_message_handler(add_link_handler, state=FSM_useful_links.to_add)
    dp.register_message_handler(del_link_handler, state=FSM_useful_links.to_delete)
    dp.register_message_handler(add_elder_handler, state=FSM_elders.to_add)
    dp.register_message_handler(del_elder_handler, state=FSM_elders.to_delete)
    dp.register_message_handler(add_cafe_handler, state=FSM_cafes.to_add)
    dp.register_message_handler(del_cafe_handler, state=FSM_cafes.to_delete)
    dp.register_message_handler(add_place_handler, state=FSM_leisure_places.to_add)
    dp.register_message_handler(del_place_handler, state=FSM_leisure_places.to_delete)
