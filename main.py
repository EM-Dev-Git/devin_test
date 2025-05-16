"""
EM_test_project - FastAPIを使用したRESTful APIアプリケーション

このファイルはアプリケーションのエントリーポイントです。
Uvicornサーバーを使用してFastAPIアプリケーションを起動します。
"""
import uvicorn

from app.main import app

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
