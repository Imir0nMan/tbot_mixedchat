from aiogram import  Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()

user_data = []


class Registration(StatesGroup):
	name = State()
	age = State()
	sex = State()
	region = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
	user_data.append(message.from_user.id)
	await message.answer("Բարև, Շարունակելու համար պետ է լրացնել քո պռոֆիլը,\nԳրիր քո անուն ազգանունը, տարիքը, սեռը և բնակության վայրը")


@router.message(Command("reg"))
async def reg_user(message: Message, state: FSMContext):
	await state.set_state(Registration.name)
	await message.answer("Անուն Ազգանուն")


@router.message(Registration.name)
async def reg_one(message: Message, state: FSMContext):
	user_data.append(message.text)
	await state.set_state(Registration.age)
	await message.answer("Տարիք")

@router.message(Registration.age)
async def reg_one(message: Message, state: FSMContext):
	user_data.append(message.text)
	await state.set_state(Registration.sex)
	await message.answer("Սեռ՝ Արական, Իգական, Այլ")


@router.message(Registration.sex)
async def reg_one(message: Message, state: FSMContext):
	user_data.append(message.text)
	await state.set_state(Registration.region)
	await message.answer("Բնակության վայր")


@router.message(Registration.region)
async def reg_one(message: Message, state: FSMContext):
	user_data.append(message.text)
	await message.answer(f'Հարցերը այսքանն էին, Շնորհակալություն\n {user_data[1]}')
	print (user_data)
	await state.clear()


