"""
アイテムのデータベースモデル

このモジュールはSQLAlchemyを使用してアイテムのデータベーステーブルを定義します。
アイテムはユーザーに所有され、名前、説明、価格、税金などの情報を持ちます。
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Item(Base):
    """
    アイテムモデル
    
    アイテムはユーザーが所有する商品や製品を表します。
    各アイテムには名前、説明、価格、税金などの属性があります。
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, comment="アイテムの一意識別子")
    name = Column(String, index=True, comment="アイテム名")
    description = Column(String, nullable=True, comment="アイテムの説明")
    price = Column(Float, comment="アイテムの価格")
    tax = Column(Float, nullable=True, comment="アイテムの税金")
    owner_id = Column(Integer, ForeignKey("users.id"), comment="所有者のユーザーID")
    
    owner = relationship("User", back_populates="items", comment="アイテムの所有者")
