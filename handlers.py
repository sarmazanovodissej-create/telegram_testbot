from db import get_pet, update_pet, create_pet

from aiogram import Dispatcher, types, F
from aiogram.filters import Command

from keyboards import (
    main_kb,
    food_kb,
    play_kb,
    BTN_FEED, 
    BTN_PLAY, 
    BTN_SLEEP, 
    BTN_STATUS
)


def progres_bar(value: int, lenght: int):
    filled = int(value/100 * 10)
    return "🟩" * filled + "⬛️" * (lenght - filled)


async def register_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command("start"))
    dp.message.register(feed_pet, F.text == BTN_FEED)
    dp.message.register(play_pet, F.text == BTN_PLAY)
    dp.message.register(status_pet, F.text == BTN_STATUS)
    dp.message.register(sleep_pet, F.text == BTN_SLEEP)
    dp.callback_query.register(food_callback_handler, lambda c: c.data.startswith("feed_"))
    dp.callback_query.register(play_callback_handler, lambda c: c.data.startswith("play_"))


async def start_handler(message: types.Message):
    user_id = message.from_user.id
    pet = await get_pet(user_id)
    if pet is None:
        await create_pet(user_id, "Pushok")
        pet = await get_pet(user_id)

    await message.answer(
        f"Привет, {message.from_user.first_name}\n"
        f"Познакомся со своим питомцем: {pet['name']}\n"
        f"Позаботься о нём!",
        reply_markup=main_kb
    )


async def feed_pet(message: types.Message):
    user_id = message.from_user.id
    pet = await get_pet(user_id)
    if not pet:
        await message.answer("Сначала запусти бота с помощью команды /start")
        return
    await message.answer(
        f"Чем вы хотите покормить {pet['name']}?",
        reply_markup=food_kb
    )


async def play_pet(message: types.Message):
    user_id = message.from_user.id
    pet = await get_pet(user_id)
    if not pet:
        await message.answer("Сначала запусти бота с помощью команды /start")
        return
    await message.answer(
        f"Чем вы хотите позаниматься с {pet['name']}?",
        reply_markup=play_kb
    )


async def status_pet(message: types.Message):
    user_id = message.from_user.id
    pet = await get_pet(user_id)
    if not pet:
        await message.answer("Сначала запусти бота с помощью команды /start")
        return
    
    hun = pet['hunger']
    en = pet['energy']
    hap = pet['happiness']
    tr = pet['training']

    status = (
        f"Статус вашего питомца {pet['name']}:\n"
        f"Сытость: {hun}% {progres_bar(hun, 10)}\n"
        f"Энергия: {en}% {progres_bar(en, 10)}\n"
        f"Счастье: {hap}% {progres_bar(hap, 10)}\n"
        f"Натрен-ть: {tr}% {progres_bar(tr, 10)}\n"
    )
    await message.answer(status)


async def sleep_pet(message: types.Message):
    user_id = message.from_user.id
    pet = await get_pet(user_id)
    if not pet:
        await message.answer("Сначала запусти бота с помощью команды /start")
        return
    pet["happiness"] = min(pet["happiness"] + 10, 100)
    pet["hunger"] = min(pet["hunger"] - 5, 100)
    pet["energy"] = max(pet["energy"] + 15, 0)

    await update_pet(
        user_id = user_id,
        name = pet["name"],
        hunger = pet["hunger"],
        happiness = pet["happiness"],
        energy = pet["energy"],
        training = pet["training"]
    )
    await message.answer(f"{pet['name']} славно выспался!")


async def food_callback_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    pet = await get_pet(user_id)
    if not pet:
        await message.answer("Сначала запусти бота с помощью команды /start")
        return
    
    food = callback.data
    message = ""
    hun = pet["hunger"]
    hap = pet["happiness"]
    en = pet["energy"]

    if food == "feed_shawarma":
        hun = pet["hunger"] + 15
        hap = pet["happiness"] + 20
        en = pet["energy"] - 5
        message = f"Вы покормили {pet['name']} вкусной шавухой!"

    elif food == "feed_steak":
        hun = pet["hunger"] + 20
        hap = pet["happiness"] + 15
        en = pet["energy"] - 5
        message = f"Вы покормили {pet['name']} вкусным стейком!"

    elif food == "feed_tea":
        hun = pet["hunger"] + 10
        hap = pet["happiness"] + 10
        en = pet["energy"] + 5
        message = f"Вы напоили {pet['name']} вкусным чаем!"

    pet["happiness"] = min(100, hap)
    pet["hunger"] = min(100, hun)
    pet["energy"] = min(100, en)

    await update_pet(
        user_id = user_id,
        name = pet["name"],
        hunger = pet["hunger"],
        happiness = pet["happiness"],
        energy = pet["energy"],
        training = pet["training"]
    )
    await callback.message.edit_text(message)
    await callback.answer(
        f"Сытость {pet['name']} -- {pet['hunger']}/100\n"
        f"{progres_bar(pet['hunger'], 10)}"
        f"Счастье {pet['name']} -- {pet['happiness']}/100\n"
        f"{progres_bar(pet['happiness'], 10)}"
        f"Энергия {pet['name']} -- {pet['energy']}/100\n"
        f"{progres_bar(pet['energy'], 10)}"
        )
    

async def play_callback_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    pet = await get_pet(user_id)
    if not pet:
        await message.answer("Сначала запусти бота с помощью команды /start")
        return
    
    play = callback.data
    message = ""
    hap = pet["happiness"]
    en = pet["energy"]
    tr = pet["training"]

    if play == "throw_the_ball":
        hap = pet["happiness"] + 15
        en = pet["energy"] - 5
        tr = pet["training"] + 10
        message = f"Вы кинули мяч, {pet['name']} бежит за ним!"

    elif play == "paddock":
        hap = pet["happiness"] + 20
        en = pet["energy"] - 10
        tr = pet["training"] + 5
        message = f"Вы выгуливаете {pet['name']}!"

    elif play == "workout":
        hap = pet["happiness"] + 10
        en = pet["energy"] - 15
        tr = pet["training"] + 20
        message = f"{pet['name']} немного подкачался!"

    pet["happiness"] = min(100, hap)
    pet["energy"] = min(100, en)
    pet["training"] = min(100, tr)

    await update_pet(
        user_id = user_id,
        name = pet["name"],
        hunger = pet["hunger"],
        happiness = pet["happiness"],
        energy = pet["energy"],
        training = pet["training"]
    )
    await callback.message.edit_text(message)
    await callback.answer(
        f"Счастье {pet['name']} -- {pet['happiness']}/100\n"
        f"{progres_bar(pet['happiness'], 10)}"
        f"Энергия {pet['name']} -- {pet['energy']}/100\n"
        f"{progres_bar(pet['energy'], 10)}"
        f"Натрен-ть {pet['name']} -- {pet['training']}/100\n"
        f"{progres_bar(pet['training'], 10)}"
        )
    
# _____________
# if user_id not in pets:
#         new_pet = {
#             "name": "Pushok",
#             "hunger": 50,
#             "energy": 50,
#             "happiness": 50,
#         }
#         pets[user_id] = new_pet

# pet = pets[user_id]
#     await message.answer(
#         f"Чем вы хотите покормить {pet['name']}?", 
#         reply_markup=food_kb
#     )