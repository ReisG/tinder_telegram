"""
    This module has the decorator that you pass before the function to
    ensure that user that use this function is registered.
    Please specify the name of this decreator when importing.
"""


from module.db_query_maker import selectQuery

def isRegistered(userId, myDatabase):
    answ = selectQuery("SELECT COUNT(id) FROM user WHERE tg_id = %s;", 
                [userId], 
                ["count"], 
                myDatabase)
    
    return answ[0]["count"] == 1


def user_must_register(myDatabase):
    """ decorator settes before an action that requires authorization """
    def decorator(func):
        async def inner(message, *args, **kwargs):
            # filtering arguments to decorating function
            # we must pass onnly arguments that decorating function receive
            # if we don't do that aiogram will think that it must include all data it has
            # including state, command argumants. This will cause an error on arguments
            func_args = func.__code__.co_varnames[:func.__code__.co_argcount]
            filtered_args = {k: v for k, v in kwargs.items() if k in func_args}

            if not isRegistered(message.from_user.id, myDatabase):
                await message.answer("Для начала стоит зарегистрироваться в системе. Введи /start, чтобы начать")
                return
            
            await func(message, *args, **filtered_args)
        return inner
    return decorator