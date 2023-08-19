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

from module.user_must_register import isRegistered, user_must_register
from module.db_query_maker import selectQuery, modifyQuery

import json
import html
import urllib.parse


@dp.message_handler(commands=["createblock"])
# @user_must_register(myDatabase)
async def create_block_command(message : types.Message):
    """
        Block used to create new block of devices
        Moves user to web app
        Can be used only if user is registered
    """
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.insert(types.KeyboardButton(
        text="Создать новый энергитический блок",
        web_app=types.WebAppInfo(url=config.BLOCK_CREATION_WEBAPP)
    ))

    await message.answer("Здесь можно создать энергитический блок", reply_markup=keyboard)

