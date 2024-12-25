from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from App.Databases.requests import orm_loose, orm_win
from App.Keyboards.Inline.coin_game_inline import coin_choice


main_image, head_image, tail_image = (
    'AgACAgIAAxkBAAILS2dfJ9x9NqYcHbVlOU-HG5Nwdk-PAALM6DEb1fr5SoAvt-7ptGgXAQADAgADeQADNgQ',
    'AgACAgIAAxkBAAILbWdfKXDBFcUcTp1PusIhdFrkSwQgAALo6DEb1fr5StapnuN4W9fjAQADAgADeAADNgQ',
    'AgACAgIAAxkBAAILY2dfKQJySuGj7XiCSCvU-DnX7fhiAALl6DEb1fr5SnB8WMrqY0MoAQADAgADeAADNgQ'
)

coin = {
    'head': head_image,
    'tail': tail_image
}

modes = {
    'easy': 1,
    'middle': 2,
    'hard': 3
}


async def game(callback: CallbackQuery):
    await callback.message.answer_photo(photo=main_image, caption=f"""
Bot flipped coin!
Head/Tail
""", reply_markup=coin_choice())


async def current_score(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(f"""
You have {data['user_wins']} wins and {data['user_looses']} looses
Bot has {data['bot_wins']} wins and {data['bot_looses']} looses
""")


async def round_game(callback: CallbackQuery):
    await callback.answer('BUM')
    flip, bot_choice, user_choice = callback.data.split('_')
    await callback.message.answer_photo(photo=coin[flip], caption=f'Coin - {flip}')
    await callback.message.answer_photo(photo=coin[user_choice], caption=f'You - {user_choice}')
    await callback.message.answer_photo(photo=coin[bot_choice], caption=f'Bot - {bot_choice}')


async def is_user_win(session: AsyncSession, callback: CallbackQuery, state: FSMContext, difficulty: str):
    data = await state.get_data()
    if data['user_wins'] == modes[difficulty]:
        await callback.message.answer('You won game!')
        await orm_win(session, callback.from_user.id, data['game'], difficulty)
        await state.update_data(bot_wins=0, bot_looses=0, user_wins=0, user_looses=0)
        return True


async def is_bot_win(session: AsyncSession, callback: CallbackQuery, state: FSMContext, difficulty: str):
    data = await state.get_data()
    if data['bot_wins'] == modes[difficulty]:
        await callback.message.answer('You loosed game!')
        await orm_loose(session, callback.from_user.id, data['game'], difficulty)
        await state.update_data(bot_wins=0, bot_looses=0, user_wins=0, user_looses=0)
        return True
