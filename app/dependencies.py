"""
認証依存関数モジュール

このモジュールはFastAPIの依存性注入システムを使用して、
JWTトークンベースの認証機能を提供します。保護されたエンドポイントで
ユーザーの認証と認可を行うための関数を定義します。
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.models.user import User
from app.utils.auth import verify_token

logger = logging.getLogger("app")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    現在のユーザーを取得する依存関数
    
    JWTトークンを検証し、対応するユーザーをデータベースから取得します。
    トークンが無効な場合や、ユーザーが存在しない場合は401エラーを返します。
    
    Args:
        token: JWTトークン（OAuth2スキームから自動的に取得）
        db: データベースセッション
        
    Returns:
        User: 認証されたユーザーオブジェクト
        
    Raises:
        HTTPException: トークンが無効またはユーザーが存在しない場合
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.username == token_data.username).first()
    
    if user is None:
        logger.warning(f"User {token_data.username} not found")
        raise credentials_exception
        
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    現在のアクティブユーザーを取得する依存関数
    
    ユーザーがアクティブ（is_active=True）であることを確認します。
    非アクティブユーザーの場合は400エラーを返します。
    
    Args:
        current_user: 認証されたユーザー（get_current_user依存関数から取得）
        
    Returns:
        User: 認証されたアクティブユーザー
        
    Raises:
        HTTPException: ユーザーが非アクティブの場合
    """
    if not current_user.is_active:
        logger.warning(f"Inactive user {current_user.username} attempted access")
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
