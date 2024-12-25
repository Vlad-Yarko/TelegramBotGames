from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from App.Middlewares.Throting import IsAdmin
from App.Databases.connect import main_session
from App.Keyboards.Inline.admin_inline import first_action, mess, edit_games
from App.FSM.base_fsm import Admin
from App.Filters.all_filters import CallDataEq
from App.Databases.requests import orm_get_user_chats, orm_add_data


admin_router = Router()
admin_router.message.outer_middleware(IsAdmin(main_session))
admin_router.callback_query.outer_middleware(IsAdmin(main_session))


# @admin_router.message(Command('quit'))
@admin_router.message(Command('admin'))
async def start_admin(message: Message, state: FSMContext):
    await state.set_state(Admin.active)
    await message.answer(f"""
Hello {message.from_user.username}!
What would you like to do?
""", reply_markup=first_action)


@admin_router.callback_query(CallDataEq('photo_id'), StateFilter(Admin.active))
async def photo_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.photo)
    await callback.message.answer('I am waiting for your photo')
    await callback.answer()


@admin_router.message(F.photo, StateFilter(Admin.photo))
async def take_photo_admin(message: Message, state: FSMContext):
    await message.answer('Good photo')
    await message.answer(message.photo[-1].file_id)
    await state.set_state(Admin.active)
    await message.answer(f"""
What would you like to do?
""", reply_markup=first_action)


@admin_router.callback_query(CallDataEq('send_message'), Admin.active)
async def send_message_users(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.send_message)
    await callback.answer()
    await callback.message.answer('What kind of message do you want to send?', reply_markup=mess)


@admin_router.callback_query(CallDataEq('text_message'), StateFilter(Admin.send_message))
async def send_text_message_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.send_text)
    await callback.message.answer("I am waiting for your message to send it")


@admin_router.callback_query(CallDataEq('photo_message'), StateFilter(Admin.send_message))
async def send_text_message_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.send_photo)
    await callback.message.answer("I am waiting for your message to send it")


@admin_router.message(StateFilter(Admin.send_text))
async def send_text_message(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    try:
        mes = message.text
        chats = await orm_get_user_chats(session)
        for chat in chats:
            await bot.send_message(chat, mes)
        await message.answer('I sent message to everyone')
        await state.set_state(Admin.active)
        await message.answer(f"""
What would you like to do?
""", reply_markup=first_action)
    except Exception:
        await message.answer('Incorrect data')
        await state.set_state(Admin.active)
        await message.answer(f"""
What would you like to do?
""", reply_markup=first_action)


@admin_router.message(StateFilter(Admin.send_photo))
async def send_photo_message(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    try:
        mes_text = message.caption
        mes_photo = message.photo[-1].file_id
        chats = await orm_get_user_chats(session)
        for chat in chats:
            await bot.send_photo(chat, photo=mes_photo, caption=mes_text)
        await message.answer('I sent message to everyone')
        await state.set_state(Admin.active)
        await message.answer(f"""
What would you like to do?
""", reply_markup=first_action)
    except Exception:
        await message.answer('Incorrect data')
        await state.set_state(Admin.active)
        await message.answer(f"""
What would you like to do?
""", reply_markup=first_action)


@admin_router.callback_query(CallDataEq('edit_games'), StateFilter(Admin.active))
async def edit_data_games(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.edit_games)
    await callback.message.answer('Select game to add data in', reply_markup=edit_games)


@admin_router.callback_query(CallDataEq('add_words'), StateFilter(Admin.edit_games))
async def edit_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.add_words)
    await callback.message.answer('Input word please')


@admin_router.message(StateFilter(Admin.add_words), F.text)
async def add_w(message: Message, session: AsyncSession):
    await orm_add_data(session, 'DataWords', message.text.strip())
    await message.answer('Good')


@admin_router.callback_query(CallDataEq('add_equations'), StateFilter(Admin.edit_games))
async def edit_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Admin.add_equations)
    await callback.message.answer('Input equation please')


@admin_router.message(StateFilter(Admin.add_equations), F.text)
async def add_e(message: Message, session: AsyncSession):
    await orm_add_data(session, 'DataSequence', message.text.strip())
    await message.answer('Good')


@admin_router.message()
async def all_m(message: Message):
    pass
