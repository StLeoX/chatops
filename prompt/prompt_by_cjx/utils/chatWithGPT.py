import openai
import json
import os

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"


# 获取 api
def get_api_key(path):
    # 可以自己根据自己实际情况实现
    # 以我为例子，我是存在一个 openai_key 文件里，json 格式
    '''
    {"api": "你的 api keys"}
    '''
    openai_key_file = path
    with open(openai_key_file, 'r', encoding='utf-8') as f:
        openai_key = json.loads(f.read())
    return openai_key['api']


openai.api_key = "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"



def gpt_create_messages_fault_desc(prompt, message, response_few_shot_text=''):
    return [
        {"role": "system", "content": prompt},
        {"role": "user", "content": "run"},
        {"role": "assistant", "content": response_few_shot_text},
        {"role": "user", "content": message}
    ]
def gpt_create_messages_suggestion(prompt):
    return [
        {"role": "user", "content": prompt},
    ]



def gpt_dialogue(prompt, question, example):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=gpt_create_messages_fault_desc(prompt, question, example),
        temperature=0.5
    )
    print(response)
    return response['choices'][0]['message']['content']

def gpt_dialogue_from_messages(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=0.1
    )
    print(response)
    return response['choices'][0]['message']['content']