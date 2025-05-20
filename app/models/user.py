"""
ユーザーのデータベースモデル

このモジュールはSQLAlchemyを使用してユーザーのデータベーステーブルを定義します。
ユーザーはアプリケーションの認証システムで使用され、アイテムを所有できます。
"""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base

class User(Base):
    """
    ユーザーモデル
    
    アプリケーションのユーザーを表します。ユーザーは認証情報を持ち、
    アイテムを所有することができます。各ユーザーはユーザー名とメールアドレスで
    一意に識別されます。
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment="ユーザーの一意識別子")
    username = Column(String, unique=True, index=True, comment="ユーザー名（一意）")
    email = Column(String, unique=True, index=True, comment="メールアドレス（一意）")
    hashed_password = Column(String, comment="ハッシュ化されたパスワード")
    is_active = Column(Boolean, default=True, comment="アカウントがアクティブかどうか")
    
    items = relationship("Item", back_populates="owner")  # ユーザーが所有するアイテム
