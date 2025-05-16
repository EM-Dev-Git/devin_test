"""
OpenAI連携用プロンプトテンプレート

このモジュールはOpenAI APIに送信するためのプロンプトテンプレートを定義します。
システムプロンプトとユーザープロンプトの形式を提供し、一貫したAI応答を生成します。
"""

SYSTEM_PROMPT = """
あなたは助けになるAIアシスタントです。ユーザーの質問に対して、簡潔で正確な回答を提供してください。
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
