from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from App.Databases.requests import orm_loose, orm_win

from random import choice

modes = {
    'easy': 5,
    'middle': 3,
    'hard': 1
}


async def current_score(message: Message, state: FSMContext, difficulty):
    data = await state.get_data()
    await message.answer(f"""
You have {modes[difficulty] - data['round']} attempts
""")


async def is_win(message: Message, session: AsyncSession, state: FSMContext, difficulty):
    data = await state.get_data()
    user_choice = message.text
    missed_num = data['missed_num']
    if user_choice == missed_num:
        await message.answer('You won game')
        await message.answer(f"The sequence was {data['equation']}")
        await orm_win(session, message.from_user.id, data['game'], difficulty)
        return True
    else:
        await message.answer('You loosed round')
    await state.update_data(round=data['round'] + 1)


async def is_loose(message, state: FSMContext, difficulty, session: AsyncSession):
    data = await state.get_data()
    if data['round'] == modes[difficulty]:
        await message.answer('You loosed game')
        await message.answer(f'The sequence was {data['equation']}')
        await orm_loose(session, message.from_user.id, data['game'], difficulty)
        return True


async def starting(message: Message, state: FSMContext, difficulty):
    data = await state.get_data()
    user_equations = data['equations']
    try:
        equation = choice(user_equations)
    except IndexError:
        await state.set_state('ChooseGameState:StatisticSequence')
        await message.answer('Sorry bro, you done game. You was returned into choose menu. You can play now!')
        return
    user_equations.remove(equation)
    sequence = '_'.join(equation.split('_')[:-1])
    missed_num = equation.split('_')[-1]
    await state.update_data(equations=user_equations, sequence=sequence,
                            missed_num=missed_num, equation=equation, round=0)
    await message.answer(f"""
The sequence is {sequence + '_&'}
You have {modes[difficulty]} attempts
""")
