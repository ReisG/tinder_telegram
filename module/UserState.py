"""
    This module is used when you need to make service use finite state machine.
    Please specify its name when it's imported
"""


from aiogram.dispatcher.filters.state import State, StatesGroup

class UserState(StatesGroup):
    """ States for FSM """
    pass