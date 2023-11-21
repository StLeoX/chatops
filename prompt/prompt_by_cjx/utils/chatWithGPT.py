import openai
import json
import os


os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"


# 获取 api
def get_api_key():
    # 可以自己根据自己实际情况实现
    # 以我为例子，我是存在一个 openai_key 文件里，json 格式
    '''
    {"api": "你的 api keys"}
    '''
    openai_key_file = 'openai_key.json'
    with open(openai_key_file, 'r', encoding='utf-8') as f:
        openai_key = json.loads(f.read())
    return openai_key['api']


openai.api_key = get_api_key()


def gpt_dialogue(prompt, question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': question}
        ],
        temperature=0.0,
    )

    print(response)

    return response['choices'][0]['message']['content']

