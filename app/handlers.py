from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.DB.requests import set_user, get_categories, get_category_items
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.DB.requests import get_item


import app.keyboards as kb
import app.DB.requests as rq

router = Router()

class Register(StatesGroup):
    name=State()
    age=State()
    number=State()

@router.message(CommandStart())
async def cmd_start(message:Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в sneaker228shop_bot!', reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def items(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    all_items = await get_category_items(category_id)  # Получение товаров из категории
    keyboard = InlineKeyboardBuilder()
    
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    
    await callback.message.edit_text("Выберите товар:", reply_markup=keyboard.adjust(2).as_markup())

@router.callback_query(F.data.startswith('item_'))
async def item(callback: CallbackQuery):
    item_id = int(callback.data.split('_')[1])
    item_data = await get_item(item_id)
    
    if item_data:
        await callback.answer('Вы выбрали товар')
        await callback.message.answer(
            f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}',
            reply_markup=await kb.back_to_categories()
        )
    else:
        await callback.message.answer("Товар не найден.")



    










