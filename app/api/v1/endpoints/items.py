"""
アイテム関連のエンドポイント

このモジュールはアイテムの作成、取得、更新、削除などの
CRUD操作を行うAPIエンドポイントを定義します。
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.api.v1.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.item import Item as ItemSchema, ItemCreate, ItemUpdate
from app.services.item_service import (
    create_item, 
    get_items, 
    get_item_by_id, 
    update_item, 
    delete_item
)
import logging

logger = logging.getLogger("app")

router = APIRouter()

@router.post("/", response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
def create_item_endpoint(
    item: ItemCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    """
    新しいアイテムを作成
    
    認証されたユーザーのアイテムを新規作成します。
    
    - **name**: アイテム名（必須）
    - **description**: アイテムの説明
    - **price**: アイテムの価格（必須）
    - **tax**: アイテムの税金
    
    作成されたアイテムはリクエストを行ったユーザーに紐づけられます。
    """
    return create_item(db, item, current_user.id)

@router.get("/", response_model=List[ItemSchema])
def read_items_endpoint(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    アイテム一覧を取得
    
    認証されたユーザーが所有するアイテムの一覧を取得します。
    
    - **skip**: スキップするアイテム数（ページネーション用、デフォルト: 0）
    - **limit**: 取得するアイテム数の上限（ページネーション用、デフォルト: 100）
    
    返される結果は現在のユーザーが所有するアイテムのみです。
    """
    return get_items(db, current_user.id, skip, limit)

@router.get("/{item_id}", response_model=ItemSchema)
def read_item_endpoint(
    item_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    特定のアイテムを取得
    
    指定されたIDのアイテムを取得します。
    
    - **item_id**: 取得するアイテムのID（パスパラメータ）
    
    アイテムが存在しない場合や、他のユーザーのアイテムにアクセスしようとした場合は
    404エラーが返されます。
    """
    item = get_item_by_id(db, item_id, current_user.id)
    if item is None:
        logger.warning(f"Item with ID {item_id} not found for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemSchema)
def update_item_endpoint(
    item_id: int, 
    item: ItemUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    アイテムを更新
    
    指定されたIDのアイテムを更新します。
    
    - **item_id**: 更新するアイテムのID（パスパラメータ）
    - **name**: 新しいアイテム名（必須）
    - **description**: 新しいアイテムの説明
    - **price**: 新しいアイテムの価格（必須）
    - **tax**: 新しいアイテムの税金
    
    アイテムが存在しない場合や、他のユーザーのアイテムを更新しようとした場合は
    404エラーが返されます。
    """
    updated_item = update_item(db, item_id, item, current_user.id)
    if updated_item is None:
        logger.warning(f"Attempted to update non-existent item with ID {item_id} for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{item_id}")
def delete_item_endpoint(
    item_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    アイテムを削除
    
    指定されたIDのアイテムを削除します。
    
    - **item_id**: 削除するアイテムのID（パスパラメータ）
    
    アイテムが存在しない場合や、他のユーザーのアイテムを削除しようとした場合は
    404エラーが返されます。
    
    削除が成功した場合は成功メッセージを返します。
    """
    success = delete_item(db, item_id, current_user.id)
    if not success:
        logger.warning(f"Attempted to delete non-existent item with ID {item_id} for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
