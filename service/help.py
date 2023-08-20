import logging

import aiogram
from aiogram import Bot, Dispatcher, types

from module.BotInitObject import dp
from module.Database import myDatabase

from module.user_must_register import user_must_register

@dp.message_handler(commands=["help"])
# @user_must_register(myDatabase)
async def help_command(message : types.Message):
    instractions = """Команды:
/registration - зарегистрироваться
/makeservicerequest - создать заявку на предоставление услуги
/cancel - отменить выполняемое действие"""
    await message.answer(instractions)