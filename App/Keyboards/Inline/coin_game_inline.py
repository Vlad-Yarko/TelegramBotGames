from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from random import choice


def coin_choice():
    coin = ('head', 'tail')
    ch = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Head', callback_data=f'{choice(coin)}_{choice(coin)}_head'),
                InlineKeyboardButton(text='Tail', callback_data=f'{choice(coin)}_{choice(coin)}_tail')
            ]
        ]
    )
    return ch
