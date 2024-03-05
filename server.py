import logging
import os
import redis
from app import create_app
from app.prompt.gpt_chat_manager import GptChatManager
import app as app2

app = create_app(debug=True)

# 通过环境变量设定 REDIS_URL
redis_url = os.environ.get("REDIS_URL", "")
if redis_url:
    # 初始化 redis 配置
    app2.the_redis = redis.from_url(redis_url)

    # 设定初始值
    app2.the_redis['aid'] = 1
    app2.the_redis['eid'] = 1
    app2.the_redis['fid'] = 1
    app2.the_redis['rid'] = 1

    print("init Redis ok")

# 通过环境变量设定 API_KEY，初始化 the_chat_manager
api_key = os.environ.get("OPENAI_API_KEY", "")
if api_key:
    app2.the_chat_manager = GptChatManager(api_key=api_key)
    print("init GPT ok")

if __name__ == "__main__":
    app.run()
