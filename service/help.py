import logging

import config

# aiogram imports
import aiogram
from aiogram import Bot, Dispatcher, types

# including module to work with Finite State Mashine in aiogram
from aiogram.dispatcher import FSMContext
from module.UserState import UserState

from module.BotInitObject import dp
from module.Database import myDatabase

from module.user_must_register import isRegistered
from module.db_query_maker import selectQuery, modifyQuery

@dp.message_handler(commands=["help"])
async def help_command(message : types.Message):
    mess = "Разрешённые команды:\n" \
            "/register Зарегистрироваться в системе"
    await message.answer(mess)