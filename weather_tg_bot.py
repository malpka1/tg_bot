import requests
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Hi, what city did you want to know the weather in?")


@dp.message_handler()
async def weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Clear ☀️',
        'Clouds': 'Clouds ☁️',
        'Rain': 'Rain 🌧',
        'Thunderstorm': 'Thunderstorm ⛈',
        'Snow': 'Snow ❄️',
        'Mist': 'Mist 🌫'
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = weather_description

        await message.reply(f'Wheather in the city: {city}\nTemp:{cur_weather} {wd}')
    except:
        await message.reply('\U00002620 Check the city name')

if __name__ == '__main__':
    executor.start_polling(dp)
