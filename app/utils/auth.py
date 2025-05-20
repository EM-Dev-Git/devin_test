"""
認証ユーティリティモジュール

このモジュールはパスワードのハッシュ化、検証、JWTトークンの生成と検証のための
ユーティリティ関数を提供します。認証システム全体の中核となる機能を実装しています。
"""
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
import logging

from app.schemas.user import TokenData

logger = logging.getLogger("app")

SECRET_KEY = "YOUR_SECRET_KEY_HERE"  # Should be stored in environment variables in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    パスワード検証関数
    
    平文パスワードとハッシュ化されたパスワードを比較して検証します。
    
    Args:
        plain_password: ユーザーが入力した平文パスワード
        hashed_password: データベースに保存されているハッシュ化パスワード
        
    Returns:
        bool: パスワードが一致する場合はTrue、それ以外はFalse
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    パスワードハッシュ化関数
    
    平文パスワードをbcryptアルゴリズムでハッシュ化します。
    
    Args:
        password: ハッシュ化する平文パスワード
        
    Returns:
        str: ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    JWTアクセストークン生成関数
    
    ユーザー情報を含むJWTトークンを生成します。
    
    Args:
        data: トークンに含めるデータ（通常はユーザー名を含む辞書）
        expires_delta: トークンの有効期限（省略時はデフォルト値を使用）
        
    Returns:
        str: 生成されたJWTトークン
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """
    JWTトークン検証関数
    
    JWTトークンを検証し、含まれるユーザー名を取得します。
    
    Args:
        token: 検証するJWTトークン
        credentials_exception: トークンが無効な場合に発生させる例外
        
    Returns:
        TokenData: トークンから取得したユーザーデータ
        
    Raises:
        credentials_exception: トークンが無効または期限切れの場合
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise credentials_exception

def decode_access_token(token: str) -> Optional[str]:
    """
    JWTアクセストークンからユーザー名を取得する
    
    JWTトークンを検証し、含まれるユーザー名を取得します。
    
    Args:
        token: 検証するJWTトークン
        
    Returns:
        str: トークンから取得したユーザー名、トークンが無効な場合はNone
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return username
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        return None
