from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

# Assuming you have already set up the bot and dispatcher
bot = Bot(token='YOUR_BOT_TOKEN')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Welcome! Choose an option:", reply_markup=main)

@dp.message_handler(lambda message: message.text == "Каталог")
async def show_categories(message: types.Message):
    await message.answer("Choose a category:", reply_markup=await categories())

@dp.callback_query_handler(lambda c: c.data.startswith('category_'))
async def category_selected(callback_query: types.CallbackQuery):
    category_id = int(callback_query.data.split('_')[1])
    await callback_query.answer()
    await callback_query.message.answer("Here are the items:", reply_markup=await items(category_id))

@dp.message_handler(lambda message: message.text == "Назад")  # Assuming you use this text
async def back_to_main(message: types.Message):
    await message.answer("Welcome back! Choose an option:", reply_markup=main)

@dp.message_handler(lambda message: message.text == "На главную")
async def return_to_main(message: types.Message):
    await message.answer("Returned to main menu:", reply_markup=main)

# Main execution
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
