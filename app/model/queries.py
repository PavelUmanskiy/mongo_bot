from datetime import datetime

from model.connection import collection


async def get_salary_data_filtered(dt_from: str, dt_upto):
    dt_from = datetime.strptime(dt_from, "%Y-%m-%dT%H:%M:%S")
    dt_upto = datetime.strptime(dt_upto, "%Y-%m-%dT%H:%M:%S")
    query = {
        'dt': {
            '$gte': dt_from,
            '$lte': dt_upto
        }
    }
    matched_documents = []
    async for document in collection.find(query):
        matched_documents.append(document)
    return matched_documents