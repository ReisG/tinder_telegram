"""
    This is a module that is called to get Bot Initialization Objects
    like bot, storage, and dp objects
    When you import it, please specify what objects are you going to use from here
"""

import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

# Initializing
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# including logging
logging.basicConfig(level=logging.INFO)