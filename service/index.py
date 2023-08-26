import logging

import aiogram
from aiogram import Bot, Dispatcher, types

from module.BotInitObject import dp
from module.Database import myDatabase

from module.user_must_register import user_must_register

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

import json
import html
import urllib.parse

@dp.message_handler(commands=["getplan"])
async def getplan_command(message : types.Message):
    await message.answer("Ваш план потребления и производства на завтра:")
    with open("grap.png", "rb") as ph:
        await message.answer_photo(types.InputFile(ph))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.insert(types.InlineKeyboardButton(
        text="Отказаться на завтра", 
        callback_data="hello"
    ))
    await message.answer("За завтра требуется выдать 17,1 кВт*ч энергии и потребить не более 10,5 кВт*ч", reply_markup=keyboard)