from aiogram import types, Dispatcher
from keyboards import menu_markup, help_markup, wishes_markup
from handlers.fsm import FSM_helps, FSM_start


async def help(message: types.Message):
    if message.text == 'Список моей группы':
        ur_group = 'Тут должно быть фото твоей группы'
        await message.answer(ur_group)
    if message.text == 'Связь с деканатом':
        deanery = 'Тут вся связь с деканатом'
        await message.answer(deanery)
    if message.text == 'Список старост':
        elders = 'Тут должен быть список старост'
        await message.answer(elders)
    if message.text == 'Ваши пожелания для бота':
        await message.answer('Введите ваши пожелания', reply_markup=wishes_markup())
        await FSM_helps.wishes.set()
    if message.text == 'Вернуться в меню':
        fio = 'Фамилия Имя Отчество'
        course = 'n-ый'
        group = '***-**'
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \n Курс: {course} \n Группа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


async def wishes(message: types.Message):
    # Тут надо добавить пожелание в БД
    if message.text == 'Вернуться в помощь':
        await message.answer('Чем помочь?', reply_markup=help_markup())
        await FSM_helps.help.set()
    else:
        await message.answer('Мы рассмотрим вашу идею', reply_markup=help_markup())
        await FSM_helps.help.set()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(help, state=FSM_helps.help)
    dp.register_message_handler(wishes, state=FSM_helps.wishes)
