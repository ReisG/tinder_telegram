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
 
@dp.message_handler(commands=["makeservicereqeust"]) 
# @user_must_register(myDatabase) 
async def make_service_request_command(message : types.Message): 
    """ 
        This method sends webapp to make_service_request 
    """ 
     
    keyboard = types.ReplyKeyboardMarkup() 
    keyboard.insert(types.KeyboardButton( 
        text="Сформировать заявку на предоставление услуги", 
        web_app=types.WebAppInfo(url=config.MAKE_SERVICE_REQUEST_WEBAPP) 
    )) 
 
    await message.answer("Сформируйте заявку на предоставление услуги", reply_markup=keyboard)


@dp.message_handler(lambda message: json.loads(message.web_app_data.data)["web_app_name"] == "make_service_request", 
                    content_types=types.ContentType.WEB_APP_DATA)
# @user_must_register(myDatabase)
async def make_service_request_webapp_handler(message : types.Message):
    """
        This module register user's request to provide chosen service
        USER MUST BE REGISTERED
        MUST INCLUDE:
            web_app_name - id of this method
            block_id - block id that request belong to
            service - name of service user want to provide
            expire_date - date when user stops provide chosen service
    """
    pass