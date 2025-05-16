from fastapi import APIRouter, HTTPException
from typing import List, Optional
import logging

from app.schemas.item import Item, ItemCreate

logger = logging.getLogger("app")

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
    logger.info(f"Item created with ID: {item_id_counter}")
    return db_item

@router.get("/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 100):
    logger.info(f"Retrieved items list with skip={skip}, limit={limit}")
    return list(items_db.values())[skip : skip + limit]

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id not in items_db:
        logger.warning(f"Item with ID {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")
    logger.info(f"Retrieved item with ID: {item_id}")
    return items_db[item_id]

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    if item_id not in items_db:
        logger.warning(f"Attempted to update non-existent item with ID {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    item_dict = item.model_dump()
    items_db[item_id] = {**item_dict, "id": item_id}
    logger.info(f"Updated item with ID: {item_id}")
    return items_db[item_id]

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items_db:
        logger.warning(f"Attempted to delete non-existent item with ID {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    logger.info(f"Deleted item with ID: {item_id}")
    return {"message": "Item deleted successfully"}
