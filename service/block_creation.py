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


@dp.message_handler(lambda message: json.loads(message.web_app_data.data)["web_app_name"] == "block_creation", 
                    content_types=types.ContentType.WEB_APP_DATA)
# @user_must_register(myDatabase)
async def create_block_webapp_prosessing(message : types.Message):
    """
        Module that creates energy block
        USER MUST BE REGISTERED
        MUST INCLUDE:
            web_app_name - id of this method
            units - list of units
                unit_type - type of installed unit
                unit_name - Model of installed unit device
                cerfiticate - certificate that was used to register unit (document_id)
                gen_power - generating unit power
                battery_capacity - capacity of installed battery (if unit_type=="storage")
                installation_date - date when unit was installed
                service_life - warranty period of installed unit
                device_status - working status of device (online, offline)
    """

    data = json.loads(message.web_app_data.data)

    # print(data)

    # loading safe data
    # process data using html library
    for i in range(len(data["units"])):
        data["units"][i]['unit_f'] = html.escape(data["units"][i]['unit_f'])
        data["units"][i]['unit_type'] = html.escape(data["units"][i]['unit_type'])
        data["units"][i]['unit_name'] = html.escape(data["units"][i]['unit_name'])
        data["units"][i]['certificate'] = html.escape(data["units"][i]['certificate'])
        data["units"][i]['gen_power'] = float(data["units"][i]['gen_power'])
        data["units"][i]['battery_capacity'] = float(data["units"][i]['battery_capacity'])
        data["units"][i]['installation_date'] = html.escape(data["units"][i]['installation_date'])
        data["units"][i]['service_life'] = int(data["units"][i]['service_life'])
        data["units"][i]['device_status'] = html.escape(data["units"][i]['device_status'])

        if data["units"][i]['unit_f'] == 'storage':
            # battery doesn't generate any power
            data["units"][i]["gen_power"] = None
        else:
            # nonbatery cannot store energy
            data["units"][i]['battery_capacity'] = None


    # moving all data from several arrays in one line
    field_order = ["unit_f", "unit_type", "unit_name", "certificate", 
                        "gen_power", "battery_capacity", 
                        "installation_date", "service_life", 
                        "device_status"]
    def data_to_line(data_array):
        res = []
        for record in data_array:
            for field in field_order:
                res.append(record[field])
        print(res)
        return res

    # Thing that we add to store one line in database
    record_template = f"({ ', '.join(['@bl_id'] + ['%s' for _ in range(len(field_order))]) })"
    
    # sending data in database all in one query
    modifyQuery("""/* Creating energy block */
                    INSERT INTO equipmentblock (user_id) VALUES ((SELECT id FROM user WHERE tg_id=%s));
                    /* getting just created block id */
                    SELECT @bl_id := LAST_INSERT_ID() FROM equipmentblock;
                    /* inserting block units */
                    INSERT INTO equipmentunit(block_id, unit_function, unit_type, unit_name, certificate, 
                            gen_power, battery_capacity, installation_date, 
                            service_life, device_status) VALUES """ + ', '.join( [record_template for i in range(len(data["units"]))] ) + ";",
                    [
                        # creating block
                        message.from_user.id,
                        # inserting block units
                        *data_to_line(data["units"])
                    ],
                    myDatabase, True)
    
    await message.answer("Данные энергитического блока записаны")