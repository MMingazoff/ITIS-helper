from aiogram import types, Dispatcher


async def echo_message(message: types.Message):
    await message.answer("Используй кнопки, я тебя не понимаю 😓")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_message, state="*")
