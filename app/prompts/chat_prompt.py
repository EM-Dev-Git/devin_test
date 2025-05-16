"""
OpenAI連携用プロンプトテンプレート

このモジュールはOpenAI APIに送信するためのプロンプトテンプレートを定義します。
システムプロンプトとユーザープロンプトの形式を提供し、一貫したAI応答を生成します。
"""

SYSTEM_PROMPT = """
あなたは助けになるAIアシスタントです。ユーザーの質問に対して、簡潔で正確な回答を提供してください。
"""

MASUI_SYSTEM_PROMPT = """
あなたはAIアシスタントです。自己紹介をする際は、あなたの機能、できること、サポートできる内容について簡潔かつ丁寧に説明してください。
"""

DEFAULT_PROMPT = """
ユーザーの質問: {user_input}
"""

def get_chat_prompt(user_input, system_prompt=SYSTEM_PROMPT):
    """
    OpenAI API用のチャットプロンプトを生成する
    
    ユーザー入力とシステムプロンプトを組み合わせて、
    OpenAI APIに送信するためのメッセージリストを生成します。
    
    Args:
        user_input: ユーザーの質問や入力
        system_prompt: AIの振る舞いを設定するシステムプロンプト（オプション）
        
    Returns:
        list: OpenAI API用のメッセージ辞書のリスト
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": DEFAULT_PROMPT.format(user_input=user_input)}
    ]
    
    return messages

def get_masui_prompt(user_name=None):
    """
    自己紹介用のチャットプロンプトを生成する
    
    ユーザー名を組み込んだ自己紹介用のプロンプトを生成します。
    ユーザー名が指定されない場合は一般的な自己紹介を生成します。
    
    Args:
        user_name: ユーザーの名前（オプション）
        
    Returns:
        list: OpenAI API用のメッセージ辞書のリスト
    """
    prompt = "自己紹介をしてください。"
    if user_name:
        prompt = f"{user_name}さんに自己紹介をしてください。"
    
    messages = [
        {"role": "system", "content": MASUI_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    return messages
