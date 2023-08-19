# importing logging
import logging

import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# preloading all necessary modules
# so that they where running at start
from module.BotInitObject import dp
from module.Database import myDatabase

# loading service modules
from service import *

# Unknown command
@dp.message_handler()
async def unknown_command(message : types.Message):
    await message.answer("Я такого не понимаю")


if __name__ == "__main__":
    # running application
    executor.start_polling(dp, skip_updates=True)