"""
アイテムCRUD機能のテスト

このモジュールはアイテムの作成、取得、更新、削除のAPIエンドポイントのテストを提供します。
"""
import pytest
from fastapi.testclient import TestClient
import time
import logging

logger = logging.getLogger("test")

@pytest.fixture
def test_create_item(authorized_client):
    """アイテム作成のテストフィクスチャ"""
    item_data = {
        "name": "テストアイテム",
        "description": "これはテスト用のアイテムです。",
        "price": 1000.0,
        "tax": 100.0
    }
    
    response = authorized_client.post("/api/v1/items/", json=item_data)
    assert response.status_code == 201
    return {
        "item_id": response.json()["id"],
        "item_data": item_data
    }

def test_create_item_endpoint(authorized_client):
    """
    ITEM-001: アイテム作成のテスト
    
    認証済みユーザーが有効なアイテムデータで新しいアイテムを作成できることを確認します。
    """
    logger.info("テスト開始: アイテム作成のテスト")
    start_time = time.time()
    
    item_data = {
        "name": "テストアイテム",
        "description": "これはテスト用のアイテムです。",
        "price": 1000.0,
        "tax": 100.0
    }
    
    response = authorized_client.post("/api/v1/items/", json=item_data)
    
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["name"] == item_data["name"]
    assert response.json()["description"] == item_data["description"]
    assert response.json()["price"] == item_data["price"]
    assert response.json()["tax"] == item_data["tax"]
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: アイテム作成のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "ITEM-001",
        "status": "成功",
        "execution_time": execution_time,
        "details": "アイテムが正常に作成されました。"
    }

def test_get_items_endpoint(authorized_client, test_create_item):
    """
    ITEM-002: アイテム一覧取得のテスト
    
    認証済みユーザーが自分のアイテム一覧を取得できることを確認します。
    """
    logger.info("テスト開始: アイテム一覧取得のテスト")
    start_time = time.time()
    
    response = authorized_client.get("/api/v1/items/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: アイテム一覧取得のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "ITEM-002",
        "status": "成功",
        "execution_time": execution_time,
        "details": f"アイテム一覧が正常に取得されました。アイテム数: {len(response.json())}"
    }

def test_get_item_endpoint(authorized_client, test_create_item):
    """
    ITEM-003: 特定アイテム取得のテスト
    
    認証済みユーザーが特定のアイテムを取得できることを確認します。
    """
    logger.info("テスト開始: 特定アイテム取得のテスト")
    start_time = time.time()
    
    item_id = test_create_item["item_id"]
    response = authorized_client.get(f"/api/v1/items/{item_id}")
    
    assert response.status_code == 200
    assert response.json()["id"] == item_id
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: 特定アイテム取得のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "ITEM-003",
        "status": "成功",
        "execution_time": execution_time,
        "details": f"アイテムID {item_id} が正常に取得されました。"
    }

def test_get_nonexistent_item_endpoint(authorized_client):
    """
    ITEM-004: 存在しないアイテム取得のテスト
    
    認証済みユーザーが存在しないアイテムを取得しようとした際に
    404エラーが返されることを確認します。
    """
    logger.info("テスト開始: 存在しないアイテム取得のテスト")
    start_time = time.time()
    
    nonexistent_id = 9999
    response = authorized_client.get(f"/api/v1/items/{nonexistent_id}")
    
    assert response.status_code == 404
    assert "detail" in response.json()
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: 存在しないアイテム取得のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "ITEM-004",
        "status": "成功",
        "execution_time": execution_time,
        "details": "存在しないアイテムIDに対して適切なエラーが返されました。"
    }

def test_update_item_endpoint(authorized_client, test_create_item):
    """
    ITEM-005: アイテム更新のテスト
    
    認証済みユーザーがアイテムを更新できることを確認します。
    """
    logger.info("テスト開始: アイテム更新のテスト")
    start_time = time.time()
    
    item_id = test_create_item["item_id"]
    update_data = {
        "name": "更新されたアイテム",
        "description": "これは更新されたアイテムです。",
        "price": 1500.0,
        "tax": 150.0
    }
    
    response = authorized_client.put(f"/api/v1/items/{item_id}", json=update_data)
    
    assert response.status_code == 200
    assert response.json()["id"] == item_id
    assert response.json()["name"] == update_data["name"]
    assert response.json()["description"] == update_data["description"]
    assert response.json()["price"] == update_data["price"]
    assert response.json()["tax"] == update_data["tax"]
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: アイテム更新のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "ITEM-005",
        "status": "成功",
        "execution_time": execution_time,
        "details": f"アイテムID {item_id} が正常に更新されました。"
    }

def test_delete_item_endpoint(authorized_client, test_create_item):
    """
    ITEM-006: アイテム削除のテスト
    
    認証済みユーザーがアイテムを削除できることを確認します。
    """
    logger.info("テスト開始: アイテム削除のテスト")
    start_time = time.time()
    
    item_id = test_create_item["item_id"]
    response = authorized_client.delete(f"/api/v1/items/{item_id}")
    
    assert response.status_code == 200
    assert "message" in response.json()
    assert "deleted successfully" in response.json()["message"]
    
    get_response = authorized_client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404
    
    execution_time = time.time() - start_time
    logger.info(f"テスト完了: アイテム削除のテスト (実行時間: {execution_time:.2f}秒)")
    
    return {
        "test_id": "ITEM-006",
        "status": "成功",
        "execution_time": execution_time,
        "details": f"アイテムID {item_id} が正常に削除されました。"
    }
