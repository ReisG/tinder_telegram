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
                org_name - наименование организации
                ogrn
                address
                inn
    """

    if isRegistered(message.from_user.id, myDatabase):
        await message.answer("Вы уже зарегистрированы в системе")
        return
    
    data = json.loads(message.web_app_data.data)

    # checking if data is empty
    # we consider that every sent field is not empty
    for field in data:
        if data[field] == "":
            await message.answer("Поля не должны быть пустыми")
            return

    if data["user_type"] == "phis":
        # physical is registering
        
        # validating data
        # and dangerous symbols must be destroied

        data["first_name"] = html.escape(data["first_name"])
        data["last_name"] = html.escape(data["last_name"])
        data["fathers_name"] = html.escape(data["fathers_name"])
        data["passport_series"] = int(data["port_series"])
        data["passport_number"] = int(data["passport_number"])
        data["address"] = html.escape(data["address"])
        data["inn"] = int(data["inn"])
        data["phone_number"] = html.escape(data["phone_number"])

        # sending data to database    
        modifyQuery("""/*creating user record and saying its type*/
                        INSERT INTO user (tg_id, type) VALUES (%s, (SELECT id FROM usertype WHERE type=%s));
                        /*writing data that are required to current user type*/
                        INSERT INTO phys_info(user_id, first_name, last_name, fathers_name,
                                                passport_series, passport_number, address, 
                                                inn, phone_number)
                                    VALUES ((SELECT id FROM user WHERE tg_id=%s), %s, %s, %s,
                                            %s, %s, %s,
                                            %s, %s);""",
                        [ 
                            # creating user's instance
                            message.from_user.id, data["user_type"],
                            # writing data that are required to current user's type
                            message.from_user.id, data["first_name"], data["last_name"], data["fathers_name"],
                            data["passport_series"], data["passport_number"], data["address"],
                            data["inn"], data["phone_number"]
                        ], myDatabase)
        
    elif data["user_type"] == "urid":
        # legal is registering

        # validating data
        data["name"] = html.escape(data["name"])
        data["ogrn"] = int(data["ogrn"])
        data["address"] = html.escape(data["address"])
        data["inn"] = int(data["inn"])
        data["phone_number"] = html.escape(data["phone_number"])

        modifyQuery("""/*creating user record and saying its type*/
                        INSERT INTO user (tg_id, type) VALUES (%s, (SELECT id FROM usertype WHERE type=%s));
                        /*writing data that are required to current user type*/
                        INSERT INTO urid_info(user_id, name, ogrn, address, inn, phone_number)
                        VALUES ((SELECT id WHERE tg_id=%s), %s, %s, %s, %s, %s);""",
                        [message.from_user.id, data["name"], data["ogrn"], data["address"], data["inn"], data["phone_number"]],
                        myDatabase)
    else:
        # error
        await message.answer("Данные повреждены. Ошибка с определением лица")
        return
    
    await message.answer("Вы успешно зарегистрированы в системе", reply_markup=types.ReplyKeyboardRemove())
    