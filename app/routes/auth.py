"""
認証機能のためのAPIルーター

このモジュールはユーザー登録とJWTトークン認証のためのエンドポイントを提供します。
ユーザー認証はOAuth2パスワードフローを使用し、JWTトークンを発行します。
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, Token
from app.utils.auth import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

logger = logging.getLogger("app")

router = APIRouter(
    prefix="/auth",
    tags=["認証"],
    responses={
        400: {"description": "ユーザー名またはメールアドレスが既に登録されています"},
        401: {"description": "認証に失敗しました"}
    },
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    新規ユーザー登録
    
    新しいユーザーアカウントを作成します。
    
    - **username**: ユーザー名（必須、一意）
    - **email**: メールアドレス（必須、一意）
    - **password**: パスワード（必須）
    
    ユーザー名またはメールアドレスが既に登録されている場合は400エラーが返されます。
    登録が成功した場合は成功メッセージを返します。
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        logger.warning(f"Registration failed: Username {user.username} already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
        
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        logger.warning(f"Registration failed: Email {user.email} already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
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
    return {"message": "User registered successfully"}

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
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed: Invalid credentials for username {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"User {user.username} logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}
