# devin_test (EM_test_project)

松岡検証環境 - テストと検証のためのFastAPIプロジェクト。

## セットアップ

1. リポジトリをクローンする
2. 仮想環境を作成する：
   ```
   python -m venv venv
   ```
3. 仮想環境を有効化する：
   - Windowsの場合： `venv\Scripts\activate`
   - UnixまたはMacOSの場合： `source venv/bin/activate`
4. 依存関係をインストールする：
   ```
   pip install -r requirements.txt
   ```

## アプリケーションの実行

以下のコマンドでアプリケーションを起動：
```
uvicorn main:app --reload
```

または、main.pyファイルを直接実行：
```
python main.py
```

APIは http://localhost:8000 で利用可能になります。

## APIドキュメント

アプリケーション実行後、以下のURLで自動生成されたAPIドキュメントにアクセスできます：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
