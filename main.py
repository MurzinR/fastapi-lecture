from uuid import UUID

from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
async def read_root():
    return {'message': 'Hello World!'}


@app.get('/tasks')
async def get_task(task_id: UUID):
    return {"id": task_id}


class Item(BaseModel):
    id: int
    name: str


class ItemResponse(BaseModel):
    name: str


@app.post(
    '/items',
    response_model=ItemResponse,
)
async def save_item(
        item: Item
) -> ItemResponse:
    return ItemResponse(name=item.name)
