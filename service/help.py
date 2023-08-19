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
        /changetimezone - изменить часовой пояс
        /changecity - изменить город
        /getevents - показать события
        /participatedevents - показать события, на которые вы зарегистрировались
        /createevent - создать событие
        /showmyevents - показать созданные вами события (с возможностью редактирования)
        /getuserslist - имена пользователей
        /cancel - отменить выполняемое действие"""
    await message.answer(instractions)