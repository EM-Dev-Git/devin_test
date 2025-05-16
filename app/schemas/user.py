"""
ユーザーとトークンのPydanticスキーマ

このモジュールはユーザー認証と管理のためのPydanticモデルを定義します。
ユーザー登録、認証トークン、トークンデータの検証と変換を行います。
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

from app.schemas.item import Item

class UserBase(BaseModel):
    """
    ユーザーの基本スキーマ
    
    すべてのユーザー関連スキーマの基底クラスです。
    ユーザーの共通属性を定義します。
    """
    username: str = Field(..., description="ユーザー名（一意）")
    email: EmailStr = Field(..., description="メールアドレス（一意）")

class UserCreate(UserBase):
    """
    ユーザー作成スキーマ
    
    新しいユーザーを登録する際に使用されるスキーマです。
    UserBaseのすべての属性を継承し、パスワードを追加します。
    """
    password: str = Field(..., description="ユーザーのパスワード（ハッシュ化されて保存）")

class User(UserBase):
    """
    ユーザーレスポンススキーマ
    
    APIレスポンスで返されるユーザーのスキーマです。
    データベースから取得したユーザーをこの形式に変換して返します。
    パスワードは含まれません。
    """
    id: int = Field(..., description="ユーザーの一意識別子")
    is_active: bool = Field(..., description="アカウントがアクティブかどうか")
    items: List[Item] = Field([], description="ユーザーが所有するアイテムのリスト")

    class Config:
        """
        Pydantic設定
        
        SQLAlchemyモデルからPydanticモデルへの変換を可能にします。
        """
        from_attributes = True

class Token(BaseModel):
    """
    認証トークンスキーマ
    
    ログイン成功時に返されるJWTトークン情報を定義します。
    """
    access_token: str = Field(..., description="JWTアクセストークン")
    token_type: str = Field(..., description="トークンタイプ（通常は'bearer'）")

class TokenData(BaseModel):
    """
    トークンデータスキーマ
    
    JWTトークンからデコードされたデータを保持するスキーマです。
    ユーザー名を含みます。
    """
    username: Optional[str] = Field(None, description="トークンに含まれるユーザー名")
