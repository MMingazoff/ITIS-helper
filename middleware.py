import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from scripts.sql import add_to_banlist
from scripts.sql import get_all_banned_users

banned_users = get_all_banned_users()
if banned_users:
    banned_users = {user for user, *args in banned_users}
else:
    banned_users = {}


def update_banlist():
    global banned_users
    banned_users = get_all_banned_users()
    if banned_users:
        banned_users = {user for user, *args in banned_users}
    else:
        banned_users = {}


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=0.01, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            return

        if user in banned_users:
            raise CancelHandler()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message
        :param message:
        """
        # Get current handler
        handler = current_handler.get()

        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(message, t)

            # Cancel current handler
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed
        :param message:
        :param throttled:
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta

        if throttled.exceeded_count >= 2:
            if add_to_banlist(message.from_user.id):
                await message.reply(f'Спамить очень некрасиво. Ты улетаешь в бан :)\n'
                                    f'Если ты считаешь, что тебя забанили по ошибке, напиши @mf_jstr')
                from create_bot import bot
                await bot.send_message(text=f'{message.from_user.mention} забанен. ID: {message.from_user.id}', chat_id=-1001603217169)
                global banned_users
                banned_users = {user for user, *args in get_all_banned_users()}

        # Sleep.
        await asyncio.sleep(delta)
