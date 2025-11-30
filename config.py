import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TG_API_KEY")

# Интервал уменьшения показателей питомца в секундах
TIME_INTERVAL = 10

DECREASE_PARAMS = {
    "hunger": -3,
    "energy": -3,
    "happiness": -1,
}