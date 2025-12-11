from aiogram import types


BTN_FEED = "🌯Покормить"
BTN_PLAY = "⚽️Поиграть"
BTN_SLEEP = "🛏Спать"
BTN_STATUS = "📜Статус"


main_kb = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="🌯Покормить"), types.KeyboardButton(text="⚽️Поиграть")],
        [types.KeyboardButton(text="🛏Спать"), types.KeyboardButton(text="📜Статус")],
    ],
    resize_keyboard=True
)

remove_kb = types.ReplyKeyboardRemove()


food_kb = types.InlineKeyboardMarkup(
    inline_keyboard= [
        [
            types.InlineKeyboardButton(text="🌯Шаурма", callback_data="feed_shawarma"),
            types.InlineKeyboardButton(text="🥩Стейк", callback_data="feed_steak")
            ],

        [
            types.InlineKeyboardButton(text="☕️Дать побулькать", callback_data="feed_tea")
            ]
    ]
)

play_kb = types.InlineKeyboardMarkup(
    inline_keyboard= [
        [
            types.InlineKeyboardButton(text="🥎Покидать мяч", callback_data="play_throw_the_ball"),
            types.InlineKeyboardButton(text="🌳Выгул", callback_data="play_paddock")
            ],

        [
            types.InlineKeyboardButton(text="🥋Тренировка", callback_data="play_workout")
            ]
    ]
)