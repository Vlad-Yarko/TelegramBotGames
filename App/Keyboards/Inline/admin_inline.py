from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


first_action = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Send message', callback_data='send_message'),
            InlineKeyboardButton(text='Take photo id', callback_data='photo_id')
        ],
        [
            InlineKeyboardButton(text='Edit games', callback_data='edit_games'),
        ]
    ]
)


mess = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='send text message', callback_data='text_message')
        ],
        [
            InlineKeyboardButton(text='send text message with photo', callback_data='photo_message')
        ]
    ]
)


edit_games = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Add words to words game', callback_data='add_words')
        ],
        [
            InlineKeyboardButton(text='Add equations to sequence game', callback_data='add_equations')
        ]
    ]
)
