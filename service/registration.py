import logging

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


@dp.message_handler(commands=["start"])
async def start_command(message : types.Message):
    if isRegistered(message.from_user.id, myDatabase):
        await message.answer("Для того, чтобы узнать, какие действия можно выпонять, откройте /help")
    else:
        await message.answer("Привет! Это энергетический тиндер. " \
                             "Я помогу сократить затраты на электроэнергию и даже помочь вам подзаработать. \n\n" \
                             "Для этого вы должны являться объектом микрогенерации " \
                             "(У вас должны быть установлены быть установлены солнечные батареи, ветряные установки) \n\n" \
                             "Я помогу зарабатывать вам больше, чем если бы вы сотрудничали напрямую со сбытовой компанией. " \
                             "Чтобы зарегистрироваться в систему введите /register")
