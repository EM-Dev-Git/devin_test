"""
アイテムサービスモジュール

このモジュールはアイテムに関するビジネスロジックを提供します。
データベース操作とAPIエンドポイントの間の処理を担当します。
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
import logging

logger = logging.getLogger("app")

def create_item(db: Session, item: ItemCreate, owner_id: int) -> Item:
    """
    新しいアイテムを作成する
    
    Args:
        db: データベースセッション
        item: 作成するアイテムのデータ
        owner_id: 所有者のユーザーID
        
    Returns:
        作成されたアイテム
    """
    logger.info(f"Creating new item: {item.name}")
    db_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        tax=item.tax,
        owner_id=owner_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info(f"Created item with ID: {db_item.id}")
    return db_item

def get_items(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
    """
    ユーザーのアイテム一覧を取得する
    
    Args:
        db: データベースセッション
        owner_id: 所有者のユーザーID
        skip: スキップするアイテム数（ページネーション用）
        limit: 取得するアイテム数の上限（ページネーション用）
        
    Returns:
        アイテムのリスト
    """
    logger.info(f"Retrieving items for user ID {owner_id} with skip={skip}, limit={limit}")
    return db.query(Item).filter(Item.owner_id == owner_id).offset(skip).limit(limit).all()

def get_item_by_id(db: Session, item_id: int, owner_id: int) -> Optional[Item]:
    """
    特定のアイテムを取得する
    
    Args:
        db: データベースセッション
        item_id: 取得するアイテムのID
        owner_id: 所有者のユーザーID
        
    Returns:
        アイテム（存在しない場合はNone）
    """
    logger.info(f"Retrieving item with ID {item_id} for user ID {owner_id}")
    return db.query(Item).filter(Item.id == item_id, Item.owner_id == owner_id).first()

def update_item(db: Session, item_id: int, item: ItemUpdate, owner_id: int) -> Optional[Item]:
    """
    アイテムを更新する
    
    Args:
        db: データベースセッション
        item_id: 更新するアイテムのID
        item: 更新するアイテムのデータ
        owner_id: 所有者のユーザーID
        
    Returns:
        更新されたアイテム（存在しない場合はNone）
    """
    logger.info(f"Updating item with ID {item_id} for user ID {owner_id}")
    db_item = db.query(Item).filter(Item.id == item_id, Item.owner_id == owner_id).first()
    if db_item is None:
        logger.warning(f"Item with ID {item_id} not found for user ID {owner_id}")
        return None
    
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    logger.info(f"Updated item with ID {item_id}")
    return db_item

def delete_item(db: Session, item_id: int, owner_id: int) -> bool:
    """
    アイテムを削除する
    
    Args:
        db: データベースセッション
        item_id: 削除するアイテムのID
        owner_id: 所有者のユーザーID
        
    Returns:
        削除が成功した場合はTrue、それ以外はFalse
    """
    logger.info(f"Deleting item with ID {item_id} for user ID {owner_id}")
    db_item = db.query(Item).filter(Item.id == item_id, Item.owner_id == owner_id).first()
    if db_item is None:
        logger.warning(f"Item with ID {item_id} not found for user ID {owner_id}")
        return False
    
    db.delete(db_item)
    db.commit()
    logger.info(f"Deleted item with ID {item_id}")
    return True
