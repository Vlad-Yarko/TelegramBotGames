from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from random import choice


def rps_choice():
    bot_choice = ('rock', 'paper', 'scissors')

    ch = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Rock', callback_data=f'{choice(bot_choice)}_rock')
            ],
            [
                InlineKeyboardButton(text='Scissors', callback_data=f'{choice(bot_choice)}_scissors')
            ],
            [
                InlineKeyboardButton(text='Paper', callback_data=f'{choice(bot_choice)}_paper')
            ],
        ]
    )
    return ch
