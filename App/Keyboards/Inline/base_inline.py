from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choose_all_games(games):
    buttons = [[InlineKeyboardButton(text=game.name, callback_data=game.callback_data)] for game in games]
    kb = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
    return kb


diff = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='easy', callback_data='easy')
        ],
        [
            InlineKeyboardButton(text='middle', callback_data='middle')
        ],
        [
            InlineKeyboardButton(text='hard', callback_data='hard')
        ]
    ],
)
