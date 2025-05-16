"""
Chat prompt templates for OpenAI integration.
"""

SYSTEM_PROMPT = """
あなたは助けになるAIアシスタントです。ユーザーの質問に対して、簡潔で正確な回答を提供してください。
"""

DEFAULT_PROMPT = """
ユーザーの質問: {user_input}
"""

def get_chat_prompt(user_input, system_prompt=SYSTEM_PROMPT):
    """
    Generate a chat prompt for OpenAI API.
    
    Args:
        user_input (str): User's question or input
        system_prompt (str, optional): System prompt to set assistant behavior
        
    Returns:
        list: List of message dictionaries for OpenAI API
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": DEFAULT_PROMPT.format(user_input=user_input)}
    ]
    
    return messages
