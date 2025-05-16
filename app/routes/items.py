from fastapi import APIRouter, HTTPException
from typing import List, Optional

from app.schemas.item import Item, ItemCreate

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Item not found"}},
)

items_db = {}
item_id_counter = 0

@router.post("/", response_model=Item)
async def create_item(item: ItemCreate):
    global item_id_counter
    item_id_counter += 1
    item_dict = item.model_dump()
    db_item = {**item_dict, "id": item_id_counter}
    items_db[item_id_counter] = db_item
    return db_item

@router.get("/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 100):
    return list(items_db.values())[skip : skip + limit]

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item_dict = item.model_dump()
    items_db[item_id] = {**item_dict, "id": item_id}
    return items_db[item_id]

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted successfully"}
