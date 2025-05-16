from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import logging
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.item import Item as ItemModel
from app.models.user import User
from app.schemas.item import Item, ItemCreate

logger = logging.getLogger("app")

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Item not found"}},
)

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    db_item = ItemModel(
        name=item.name,
        description=item.description,
        price=item.price,
        tax=item.tax,
        owner_id=current_user.id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info(f"Item created with ID: {db_item.id} by user {current_user.username}")
    return db_item

@router.get("/", response_model=List[Item])
def read_items(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    items = db.query(ItemModel).filter(ItemModel.owner_id == current_user.id).offset(skip).limit(limit).all()
    logger.info(f"Retrieved items list for user {current_user.username} with skip={skip}, limit={limit}")
    return items

@router.get("/{item_id}", response_model=Item)
def read_item(
    item_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    item = db.query(ItemModel).filter(ItemModel.id == item_id, ItemModel.owner_id == current_user.id).first()
    if item is None:
        logger.warning(f"Item with ID {item_id} not found for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Item not found")
    logger.info(f"Retrieved item with ID: {item_id} for user {current_user.username}")
    return item

@router.put("/{item_id}", response_model=Item)
def update_item(
    item_id: int, 
    item: ItemCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id, ItemModel.owner_id == current_user.id).first()
    if db_item is None:
        logger.warning(f"Attempted to update non-existent item with ID {item_id} for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    logger.info(f"Updated item with ID: {item_id} for user {current_user.username}")
    return db_item

@router.delete("/{item_id}")
def delete_item(
    item_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id, ItemModel.owner_id == current_user.id).first()
    if db_item is None:
        logger.warning(f"Attempted to delete non-existent item with ID {item_id} for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    logger.info(f"Deleted item with ID: {item_id} for user {current_user.username}")
    return {"message": "Item deleted successfully"}
