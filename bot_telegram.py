from aiogram.utils import executor
from create_bot import dp, loop
from handlers import client, admin, other, commands
from scripts.autodownloader import scheduled_download

commands.register_commands(dp)
client.register_handlers(dp)
admin.register_handlers(dp)
other.register_handlers(dp)
scheduled_download()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=loop)
