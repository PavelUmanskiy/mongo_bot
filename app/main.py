import asyncio
import os
import json

import aiogram
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import Message, ContentType
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from config.constants import BASE_DIR
from model.queries import get_salary_data_filtered
from utils.custom_filters import ContentTypeFilter
from utils.data_processing import create_salary_df, aggregate_salary_data


SAMPLE_COLLECTION = BASE_DIR / 'dump/sampleDB/sample_collection.bson'
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError('.env not found')

TOKEN = os.getenv('BOT_TOKEN')
dp = aiogram.Dispatcher()
session = AiohttpSession()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    response_text = (
        "Привет, я - бот для тестового задания.\n"
        "Вот ссылка на моего создателя: @misty_light"
    )
    await message.answer(response_text)


@dp.message(ContentTypeFilter(ContentType.TEXT))
async def text_handler(message: Message) -> None:
    # message example:
    # {
    #     "dt_from": "2022-09-01T00:00:00",
    #     "dt_upto": "2022-12-31T23:59:00",
    #     "group_type": "month"
    # }
    try:
        request_data = json.loads(message.text)
    except json.JSONDecodeError as _:
        response_text = (
            "Не удалось преобразовать запрос в JSON, попробуйте ещё раз"
        )
        await message.answer(response_text)
        return
    
    group_type = request_data['group_type']
    dt_from = request_data['dt_from']
    dt_upto = request_data['dt_upto']
    
    salary_data = await get_salary_data_filtered(dt_from, dt_upto)
    salary_df = create_salary_df(salary_data)
    
    
    processed_salary_data = aggregate_salary_data(
        salary_df,
        dt_from,
        dt_upto,
        group_type
    )
    response_text = json.dumps(processed_salary_data)
    await message.answer(response_text)


@dp.message()
async def wildcard_handler(message: Message) -> None:
    response_text = (
        "На данный момент я принимаю только текстовые сообщения, построенные по"
        " формату JSON следующего типа:\n"
        "{\n"
        '   "dt_from": <type ISO datetime str>\n'
        '   "dt_upto": <type ISO datetime str>\n'
        '   "group_type": <type str choices=["hour", "day", "month"]>\n'
        "}"
        
    )
    await message.answer(response_text)


async def main() -> None:
    print('Starting...')
    bot = aiogram.Bot(TOKEN, session=session)
    await dp.start_polling(bot)   


if __name__ == "__main__":
    asyncio.run(main())
