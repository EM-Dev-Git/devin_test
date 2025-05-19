"""
API v1ルーターモジュール

このモジュールはAPIバージョン1のルーターを定義し、
各エンドポイントモジュールからルーターを集約します。
"""
from fastapi import APIRouter

from app.api.v1.endpoints import items, auth, llm

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router, prefix="/auth", tags=["認証"])
router.include_router(items.router, prefix="/items", tags=["アイテム"])
router.include_router(llm.router, prefix="/llm", tags=["LLM"])
