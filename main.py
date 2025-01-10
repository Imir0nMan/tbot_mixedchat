from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
import asyncio

# Bot token
TOKEN = "7388691014:AAGnqBSf9NHKEfau5c2AkWYevbQf3LwSuh8"

# Initialize bot with default properties
default_properties = DefaultBotProperties(parse_mode="Markdown")
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session, default=default_properties)

# Initialize dispatcher
dp = Dispatcher()
router = Router()

# In-memory storage for user data
user_data = {}

ASK_INTERESTS, ASK_GROUP_SIZE = range(1, 3)

@router.message(lambda message: message.chat.type == "private" or bot.id in [user.user.id for user in message.entities or []])
async def handle_mention(message: Message):
    user_id = message.from_user.id
    # Check if the user is already in the middle of a process
    if user_id in user_data and "step" in user_data[user_id]:
        # Do nothing; let the other handlers take over
        return

    # Greet and start the process for new users
    await message.reply("Hello! Let’s get started. What are your interests? (comma-separated)")
    user_data[user_id] = {}
    user_data[user_id]['step'] = ASK_INTERESTS


@router.message(lambda message: user_data.get(message.from_user.id, {}).get('step') == ASK_INTERESTS)
async def handle_interests(message: Message):
    user_id = message.from_user.id
    
    print ("Are you a Bitch ?")

    # Process interests
    interests = message.text.split(",")
    user_data[user_id]["interests"] = [i.strip() for i in interests]
    user_data[user_id]['step'] = ASK_GROUP_SIZE

    await message.reply("What group size do you prefer? (2-6)")


@router.message(lambda message: user_data.get(message.from_user.id, {}).get('step') == ASK_GROUP_SIZE)
async def handle_group_size(message: Message):
    try:
        user_id = message.from_user.id

        # Parse and validate group size
        group_size = int(message.text)
        if group_size < 2 or group_size > 6:
            raise ValueError()

        # Save group size and complete the process
        user_data[user_id]["group_size"] = group_size
        await message.reply(f"Group created with size {group_size}!")

        # Clear user data
        user_data.pop(user_id, None)

    except ValueError:
        await message.reply("Please enter a valid number between 2 and 6.")


# Asynchronous main function
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Run the bot
if __name__ == "__main__":
    asyncio.run(main())

