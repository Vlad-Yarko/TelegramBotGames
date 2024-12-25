from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from random import choice

from App.Databases.requests import (
    orm_win,
    orm_loose
)


letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z')

modes = {
    'easy': 20,
    'middle': 15,
    'hard': 10
}


async def starting(message: Message, state: FSMContext, difficulty):
    data = await state.get_data()
    user_words = data['words']
    try:
        word = choice(user_words)
    except IndexError:
        await state.set_state('ChooseGameState:StatisticWords')
        await message.answer('Sorry bro, you done game. You was returned into choose menu. You can play now!')
        return
    user_words.remove(word)
    await state.update_data(main_word=word, word=word, encrypted_word='^' * len(word), words=user_words,
                            wins=0, looses=0, round=0, remaining=len(word))
    await message.answer(f"""
The word is {'^' * len(word)}
You have {modes[difficulty]} attempt
""")


async def current_score(message: Message, state: FSMContext, difficulty):
    data = await state.get_data()
    await message.answer(f"""
Word is {data['encrypted_word']}
You guessed {data['wins']} letters
You loosed {data['looses']} times
You have to guess {data['remaining']} letters
You have {modes[difficulty] - data['round']} attempts
""")
    await message.answer(f"Input one letter or entire word")


async def command_score(message: Message, state: FSMContext, difficulty):
    data = await state.get_data()
    await message.answer(f"""
Word is {data['encrypted_word']}
You guessed {data['wins']} letters
You loosed {data['looses']} times
You have to guess {data['remaining']} letters
You have {modes[difficulty] - data['round']} attempts
""")


async def guess_let(message: Message, state: FSMContext, difficulty, session: AsyncSession):
    data = await state.get_data()

    user_letter = message.text.lower()
    word1 = data['word']

    if user_letter in word1:
        ind_let = word1.index(user_letter)
        word = word1.replace(user_letter, '-', 1)

        encr_word_lst = list(data['encrypted_word'])
        encr_word_lst[ind_let] = user_letter
        encrypted_word = ''.join(encr_word_lst)

        await state.update_data(wins=data['wins'] + 1, remaining=data['remaining'] - 1, word=word,
                                encrypted_word=encrypted_word)
        await message.answer('Yes bro!')

        main_word = data['main_word']
        if main_word == encrypted_word:
            await message.answer('You won game!')
            await message.answer(f"The word was {data['main_word']}")
            await orm_win(session, message.from_user.id, data['game'], difficulty)
            return True
    else:
        await message.answer('No bro!')
        await state.update_data(looses=data['looses'] + 1)
    await state.update_data(round=data['round'] + 1)


async def is_loose(message, state: FSMContext, difficulty, session: AsyncSession):
    data = await state.get_data()
    if data['round'] == modes[difficulty]:
        await message.answer('You loosed game')
        await message.answer(f'The word was {data['main_word']}')
        await orm_loose(session, message.from_user.id, data['game'], difficulty)
        return True


async def guess_w(message: Message, state: FSMContext, difficulty, session: AsyncSession):
    data = await state.get_data()
    user_word = message.text.lower()
    main_word = data['main_word']
    if user_word == main_word:
        await message.answer('You won game!')
        await message.answer(f"The word was {main_word}")
        await orm_win(session, message.from_user.id, data['game'], difficulty)
        return True
    else:
        await message.answer('No bro!')
        await state.update_data(looses=data['looses'] + 1, round=data['round'] + 1)
