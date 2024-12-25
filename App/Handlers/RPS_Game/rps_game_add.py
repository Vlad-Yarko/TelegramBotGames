from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from App.Keyboards.Inline.rps_game_inline import rps_choice
from App.Databases.requests import orm_loose, orm_win

main_image, scissors_image, rock_image, paper_image = (
    'AgACAgIAAxkBAAIBOWdLGDeYtCSjlZ7aGycE-uzDMdyeAAJ86DEb6YpZSmiOm3JWLpJJAQADAgADeAADNgQ',
    'AgACAgIAAxkBAAIBkmdLMN27Gemvyk1jtb3gQDhOBWQYAAIz5jEbLTlYSs7sltOa1Oi9AQADAgADeAADNgQ',
    'AgACAgIAAxkBAAIBlGdLMYeWu01zcCi_21X3FVfQknDRAAI45jEbLTlYSo83FdnllzBPAQADAgADeAADNgQ',
    'AgACAgIAAxkBAAIBlGdLMYeWu01zcCi_21X3FVfQknDRAAI45jEbLTlYSo83FdnllzBPAQADAgADeAADNgQ')

images = {
    'scissors': scissors_image,
    'rock': rock_image,
    'paper': paper_image
}

modes = {
    'easy': 1,
    'middle': 2,
    'hard': 3
}


async def game(callback: CallbackQuery):
    bot_choice, user_choice = callback.data.split('_')
    await callback.message.answer_photo(photo=images[user_choice],
                                        caption=f"You - {user_choice}")
    await callback.message.answer_photo(photo=images[bot_choice],
                                        caption=f"Bot - {bot_choice}")


async def choice(callback: CallbackQuery):
    await callback.message.answer_photo(photo=main_image,
                                        caption="Choose rock/scissors/paper",
                                        reply_markup=rps_choice())


async def user_loose(callback: CallbackQuery, difficulty, session, state: FSMContext):
    data = await state.get_data()
    bot_wins = data['bot_wins'] + 1
    user_looses = data['user_looses'] + 1
    await state.update_data(
        bot_wins=bot_wins,
        user_looses=user_looses
    )
    await callback.message.answer(f"""
Loose!
Your score - {data['user_wins']}
Bot's score - {bot_wins}
    """)
    if bot_wins == modes[difficulty]:
        await callback.message.answer('You loosed game')
        await state.update_data(bot_wins=0, bot_looses=0, user_wins=0, user_looses=0)
        await orm_loose(session, callback.from_user.id, data['game'], difficulty)
    await callback.answer('Loose')


async def user_win(callback: CallbackQuery, difficulty, session, state: FSMContext):
    data = await state.get_data()
    user_wins = data['user_wins'] + 1
    bot_looses = data['bot_looses'] + 1
    await state.update_data(
        user_wins=user_wins,
        bot_looses=bot_looses
    )
    await callback.message.answer(f"""
Win!
Your score - {user_wins}
Bot's score - {data['bot_wins']}
""")
    if user_wins == modes[difficulty]:
        await callback.message.answer('You won game')
        await state.update_data(bot_wins=0, bot_looses=0, user_wins=0, user_looses=0)
        await orm_win(session, callback.from_user.id, data['game'], difficulty)
    await callback.answer('Win')


async def user_draw(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(f"""
Draw!
Your score - {data['user_wins']}
Bot's score - {data['bot_wins']}
""")
    await callback.answer('Draw')
