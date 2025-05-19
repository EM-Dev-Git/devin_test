"""
アイテムのPydanticスキーマ

このモジュールはアイテムのデータ検証と変換のためのPydanticモデルを定義します。
これらのモデルはAPIリクエストとレスポンスのデータ構造を定義し、
SQLAlchemyモデルとの変換を行います。
"""
from typing import Optional
from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    """
    アイテムの基本スキーマ
    
    すべてのアイテム関連スキーマの基底クラスです。
    アイテムの共通属性を定義します。
    """
    name: str = Field(..., description="アイテム名")
    description: Optional[str] = Field(None, description="アイテムの説明")
    price: float = Field(..., description="アイテムの価格", gt=0)
    tax: Optional[float] = Field(None, description="アイテムの税金")

class ItemCreate(ItemBase):
    """
    アイテム作成スキーマ
    
    新しいアイテムを作成する際に使用されるスキーマです。
    ItemBaseのすべての属性を継承します。
    """
    pass

class ItemUpdate(ItemBase):
    """
    アイテム更新スキーマ
    
    既存のアイテムを更新する際に使用されるスキーマです。
    ItemBaseのすべての属性を継承します。
    """
    pass

class Item(ItemBase):
    """
    アイテムレスポンススキーマ
    
    APIレスポンスで返されるアイテムのスキーマです。
    データベースから取得したアイテムをこの形式に変換して返します。
    """
    id: int = Field(..., description="アイテムの一意識別子")

    class Config:
        """
        Pydantic設定
        
        SQLAlchemyモデルからPydanticモデルへの変換を可能にします。
        """
        from_attributes = True
