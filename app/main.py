"""
EM_test_project - FastAPIアプリケーションのメインモジュール

このモジュールはFastAPIアプリケーションの設定、ミドルウェア、ルーターの登録、
およびベースエンドポイントの定義を行います。SQLiteデータベース、認証機能、
ロギング機能、およびOpenAI連携機能を統合しています。
"""
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
import os
from datetime import datetime

from app.database import engine, Base
from app.routes.items import router as items_router
from app.routes.auth import router as auth_router
from app.routes.llm import router as llm_router

Base.metadata.create_all(bind=engine)

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

log_filename = f"logs/app_{datetime.now().strftime('%Y-%m-%d')}.log"
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app_logger = logger

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    HTTPリクエストのロギングミドルウェア
    
    すべてのリクエストのメソッド、パス、ステータスコード、処理時間をログに記録します。
    """
    start_time = time.time()
    
    method = request.method
    path = request.url.path
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    app_logger.info(f"{method} {path} - Status: {response.status_code} - Time: {process_time:.4f}s")
    
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

app_logger.info("Application startup: CORS middleware configured")

app.include_router(auth_router)
app_logger.info("Application startup: Auth router registered")

app.include_router(items_router)
app_logger.info("Application startup: Item router registered")

app.include_router(llm_router)
app_logger.info("Application startup: LLM router registered")

@app.get("/", tags=["基本"])
async def root():
    """
    ルートエンドポイント
    
    アプリケーションのウェルカムメッセージを返します。
    """
    app_logger.info("Root endpoint accessed")
    return {"message": "Welcome to EM_test_project API"}

@app.get("/health", tags=["基本"])
async def health_check():
    """
    ヘルスチェックエンドポイント
    
    アプリケーションの稼働状態を確認するためのエンドポイントです。
    """
    app_logger.info("Health check endpoint accessed")
    return {"status": "healthy"}
