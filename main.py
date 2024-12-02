import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.DB.models import async_main


async def main():
    await async_main()
    bot = Bot(token='8136253392:AAHmv2Th8R-iuuEnecNO0g5MtJMbOpipSRY')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
