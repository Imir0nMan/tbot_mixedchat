import asyncio
import logging

from aiogram import Bot, Dispatcher 

from const import TOKEN
from app.handlers import router

# Initialize bot with default properties
bot = Bot(token=TOKEN)


# Initialize dispatcher
dp = Dispatcher()

# Asynchronous main function
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


# Run the bot
if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("Exit")
		
