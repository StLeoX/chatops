import logging
import os
from app import create_app
from app.prompt.gpt_chat_manager import GptChatManager
import app as app2

app = create_app(debug=True)

# 如果通过环境变量设定 API_KEY，那么直接初始化 the_chat_manager
api_key = os.environ.get("OPENAI_API_KEY", "")
if api_key:
    app2.the_chat_manager = GptChatManager(api_key=api_key)
    logging.info("init the_chat_manager with ENV api_key")

if __name__ == "__main__":
    app.run()
