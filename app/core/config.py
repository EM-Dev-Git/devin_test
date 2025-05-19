"""
アプリケーション設定モジュール

このモジュールは.envファイルから環境変数を読み込み、アプリケーション全体で使用される
設定値を一元管理します。APIキーやエンドポイントURLなどの機密情報を安全に管理します。
"""
from pydantic import BaseSettings, Field
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "env", ".env"))

class Settings(BaseSettings):
    """
    アプリケーション設定クラス
    
    このクラスは.envファイルと環境変数から設定を読み込み、
    設定値に型安全なアクセスを提供します。
    """
    APP_NAME: str = "EM_test_project"
    APP_DESCRIPTION: str = "FastAPIを使用したRESTful APIアプリケーション（SQLite認証とOpenAI連携機能付き）"
    APP_VERSION: str = "0.2.0"
    
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    OPENAI_API_BASE: Optional[str] = Field(default=None, env="OPENAI_API_BASE")
    OPENAI_API_MODEL: str = Field(default="gpt-3.5-turbo", env="OPENAI_API_MODEL")
    
    class Config:
        env_file = os.path.join("env", ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
