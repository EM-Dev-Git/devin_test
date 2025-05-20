"""
認証関連の依存関係

このモジュールは認証に関する依存関係関数を提供します。
ユーザー認証やアクセス制御に使用されます。
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import logging

from app.db.session import get_db
from app.models.user import User
from app.utils.auth import decode_access_token

logger = logging.getLogger("app")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    現在のユーザーを取得する
    
    JWTトークンからユーザー名を取得し、データベースからユーザー情報を取得します。
    
    Args:
        token: JWTトークン
        db: データベースセッション
        
    Returns:
        現在のユーザー
        
    Raises:
        HTTPException: トークンが無効な場合や、ユーザーが存在しない場合
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = decode_access_token(token)
    if username is None:
        logger.warning("Invalid token detected")
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        logger.warning(f"User not found for username: {username}")
        raise credentials_exception
    
    logger.debug(f"Current user retrieved: {username}")
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    現在のアクティブユーザーを取得する
    
    現在のユーザーがアクティブかどうかを確認します。
    
    Args:
        current_user: 現在のユーザー
        
    Returns:
        現在のアクティブユーザー
        
    Raises:
        HTTPException: ユーザーが非アクティブの場合
    """
    if not current_user.is_active:
        logger.warning(f"Inactive user attempted access: {current_user.username}")
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user
