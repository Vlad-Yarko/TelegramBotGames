from aiogram import Bot, Dispatcher

from dotenv import load_dotenv, find_dotenv

import os

from asyncio import run

from App.cmds import commands

load_dotenv(find_dotenv())

from Databases.connect import engine_begin

from App.Handlers.base_commands import base_command_router
from App.Handlers.admin_commands import admin_router
from App.Handlers.choose_game_cmd import choose_router_main, choose_router_add
from App.Handlers.RPS_Game.rps_game_main import r_p_s_router, r_p_s_router_main
from App.Handlers.Words_Game.words_game_main import words_router, words_router_main
from App.Handlers.Coin_Game.coin_game_main import coin_router_main, coin_router
from App.Handlers.Sequence_Game.sequence_game_main import sequence_router_main, sequence_router


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_routers(
    base_command_router,
    choose_router_main,
    choose_router_add,
    r_p_s_router_main,
    r_p_s_router,
    words_router_main,
    words_router,
    coin_router_main,
    coin_router,
    sequence_router_main,
    sequence_router,
    admin_router
)


async def main():
    await engine_begin()
    await bot.set_my_commands(commands=commands)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    run(main())
