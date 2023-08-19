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


@dp.message_handler(commands=["start"])
async def start_command(message : types.Message):
    if isRegistered(message.from_user.id, myDatabase):
        await message.answer("Для того, чтобы узнать, какие действия можно выпонять, откройте /help")
    else:
        await message.answer("Привет! Это энергетический тиндер. " \
                             "Я помогу сократить затраты на электроэнергию и даже помочь вам подзаработать. \n\n" \
                             "Для этого вы должны являться объектом микрогенерации " \
                             "(У вас должны быть установлены солнечные батареи, ветряные установки) \n\n" \
                             "Я помогу зарабатывать вам больше, чем если бы вы сотрудничали напрямую со сбытовой компанией. " \
                             "Чтобы зарегистрироваться в систему введите /register")


@dp.message_handler(commands=["register"])
async def register_command(message : types.Message):
    """
        This module used to register user in system
    """
    if isRegistered(message.from_user.id, myDatabase):
        await message.reply("Вы уже зарегистрированы в системе")
        return

    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.insert(types.KeyboardButton(
        text="Заполнить форму регистрации",
        web_app=types.WebAppInfo(url=config.USER_REGISTRATION_WEBAPP)
    ))
    await message.answer("Заполните форму для регистрации в приложении", reply_markup=keyboard)


@dp.message_handler(lambda message: json.loads(message.web_app_data.data)["web_app_name"] == "user_registration", 
                    content_types=types.ContentType.WEB_APP_DATA)
async def user_registration_webapp_prosessing(message : types.Message):
    """
        Registration user webapp handler
        !!!USER MUST NOT BE REGISTERED ALREADY!!!
        !!!DATA MUST BE VALID!!!
        MUST INCLUDE:
            web_app_name - id of this method
            user_type - тип пользователя (phisical or legal)
            physical:
                first_name
                last_name
                fathers_name
                passport_series
                passport_number
                address
                inn
                phone_number
            legal:
                org_name - 
    """

    if isRegistered(message.from_user.id, myDatabase):
        await message.answer("Вы уже зарегистрированы в системе")
        return
    
    data = json.loads(message.web_app_data.data)
    