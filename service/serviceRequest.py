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
        block must exist and user must own it 
        MUST INCLUDE: 
            web_app_name - id of this method 
            block_id - block id that request belong to 
            service - name of service user want to provide 
            expire_date - date when user stops provide chosen service 
    """ 
     
    data = json.loads(message.web_app_data.data) 
 
    # validating data 
    data["web_app_name"] = html.escape(data['web_app_name']) 
    data["block_id"] = int(data['block_id']) 
    data["service"] = html.escape(data['service']) 
    data["expire_date"] = html.escape(data['expire_date']) 
 
    # block existance checking 
    resp = selectQuery("""SELECT COUNT(id)  
                            FROM equipmentblock as b 
                            LEFT JOIN user as u ON b.user_id=u.id WHERE u.tg_id=%s AND b.id=%s;""", 
                            [message.from_user.id, data["block_id"]], ["count"], myDatabase) 
     
    resp = resp[0] 
    if resp['count'] < 1: 
        await message.answer("Данного энергитического блока не найдено") 
        return 
    elif resp['count'] > 1: 
        await message.answer("ОШИБКА. Найдено несколько энергитических блоков...") 
        # log an error 
        return 
     
    # writing to db 
    modifyQuery("""INSERT INTO servicerequest(block_id, service, expire_date, status)  
                    VALUES (%s, (SELECT id FROM servicetype WHERE type=%s), %s, "pending");""", 
                    [data["block_id"], data["service"], ], myDatabase) 
     
    await message.answer("Заявка успешно сформирована", reply_markup=types.ReplyKeyboardRemove())
