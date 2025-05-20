"""
認証サービスモジュール

このモジュールは認証に関するビジネスロジックを提供します。
ユーザー登録、認証、トークン生成などの処理を担当します。
"""
from datetime import timedelta
from sqlalchemy.orm import Session
from typing import Optional

from app.models.user import User
from app.schemas.user import UserCreate, Token
from app.utils.auth import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
import logging

logger = logging.getLogger("app")

def register_user(db: Session, user: UserCreate) -> bool:
    """
    新規ユーザーを登録する
    
    Args:
        db: データベースセッション
        user: 登録するユーザーのデータ
        
    Returns:
        登録が成功した場合はTrue、それ以外はFalse
        
    Raises:
        ValueError: ユーザー名またはメールアドレスが既に登録されている場合
    """
    logger.info(f"Registering new user: {user.username}")
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        logger.warning(f"Registration failed: Username {user.username} already registered")
        raise ValueError("Username already registered")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        logger.warning(f"Registration failed: Email {user.email} already registered")
        raise ValueError("Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"User {user.username} registered successfully")
    return True

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    ユーザーを認証する
    
    Args:
        db: データベースセッション
        username: ユーザー名
        password: パスワード
        
    Returns:
        認証に成功した場合はユーザーオブジェクト、それ以外はNone
    """
    logger.info(f"Authenticating user: {username}")
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        logger.warning(f"Authentication failed for user: {username}")
        return None
    
    logger.info(f"User {username} authenticated successfully")
    return user

def create_user_token(user: User) -> Token:
    """
    ユーザーのアクセストークンを作成する
    
    Args:
        user: ユーザーオブジェクト
        
    Returns:
        アクセストークン情報
    """
    logger.info(f"Creating access token for user: {user.username}")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
