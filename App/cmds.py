from aiogram.types import BotCommand

commands = [
    BotCommand(command='start', description='start bot'),
    BotCommand(command='help', description='list of commands'),
    BotCommand(command='select', description='select game'),
    BotCommand(command='statistics', description='see all statistics'),
    BotCommand(command='score', description='see current score'),
    BotCommand(command='quit', description='quit current game'),
    BotCommand(command='start_game', description='start game'),
    BotCommand(command='difficulty', description='choose difficulty'),
    BotCommand(command='rules', description='see rules of selected game'),
    BotCommand(command='menu', description='return to menu'),
    BotCommand(command='admin', description='Only for admins')
]
