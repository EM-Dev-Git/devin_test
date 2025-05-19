"""
認証関連のエンドポイント

このモジュールはユーザー登録とJWTトークン認証のためのエンドポイントを提供します。
ユーザー認証はOAuth2パスワードフローを使用し、JWTトークンを発行します。
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging

from app.db.session import get_db
from app.schemas.user import UserCreate, Token
from app.services.auth_service import register_user, authenticate_user, create_user_token

logger = logging.getLogger("app")

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dict)
def register_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    """
    新規ユーザー登録
    
    新しいユーザーアカウントを作成します。
    
    - **username**: ユーザー名（必須、一意）
    - **email**: メールアドレス（必須、一意）
    - **password**: パスワード（必須）
    
    ユーザー名またはメールアドレスが既に登録されている場合は400エラーが返されます。
    登録が成功した場合は成功メッセージを返します。
    """
    try:
        register_user(db, user)
        return {"message": "User registered successfully"}
    except ValueError as e:
        logger.warning(f"Registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    アクセストークンの取得（ログイン）
    
    ユーザー名とパスワードを使用してJWTアクセストークンを取得します。
    このエンドポイントはOAuth2パスワードフローを使用しています。
    
    - **username**: ユーザー名（フォームデータ）
    - **password**: パスワード（フォームデータ）
    
    認証に成功すると、JWTアクセストークンが返されます。
    このトークンは他のAPIエンドポイントへのアクセスに使用できます。
    
    認証に失敗した場合は401エラーが返されます。
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Login failed: Invalid credentials for username {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return create_user_token(user)
