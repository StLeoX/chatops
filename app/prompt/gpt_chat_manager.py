import re
import time
import logging

import openai
from openai.types.chat import ChatCompletion

import app
from app.config.dev import *
from .prompt_manager import *


class GptChatManager:
    def __init__(self, api_key: str = "", base_url: str = ""):
        """
        api_key: default in env
        """

        if api_key:
            self._api_key = api_key
        else:
            self._api_key = os.environ.get("OPENAI_API_KEY", "")
        if not self._api_key:
            logging.fatal("`OPENAI_API_KEY` not set")

        if base_url:
            self._base_url = base_url
        else:
            self._base_url = os.environ.get("BASE_URL", "")
        if not self._base_url:
            logging.fatal("`BASE_URL` not set")

        self._model_kind = DEFAULT_MODEL

        [getattr(self, method)() for method in dir(self) if
         callable(getattr(self, method)) and re.match(r'_new.*_chat', method)]

    def _new_general_chat(self):
        # 预热普通对话
        # 缺省网络连接配置：超时 3s, 重连 2 次
        if self._base_url:
            self._general_chat = openai.OpenAI(api_key=self._api_key, base_url=self._base_url, timeout=3,
                                               max_retries=2).chat
        else:
            self._general_chat = openai.OpenAI(api_key=self._api_key, timeout=3, max_retries=2).chat

    def _new_fault_desc_chat(self):
        # 预热对话
        # 网络连接配置：超时 3s, 重连 2 次
        self._fault_desc_chat = openai.OpenAI(api_key=self._api_key, base_url=self._base_url, timeout=3,
                                              max_retries=2).chat
        self._do_gpt_chat(self._fault_desc_chat, get_pre_hot_fault_desc(), 'system')

    def _new_expectation_chat(self):
        # 预热对话
        # 网络连接配置：超时 3s, 重连 2 次
        self._expectation_chat = openai.OpenAI(api_key=self._api_key, base_url=self._base_url, timeout=3,
                                               max_retries=2).chat
        self._do_gpt_chat(self._expectation_chat, get_pre_hot_expectation(), 'system')

    def _new_fault_report_chat(self):
        # 预热对话
        # 网络连接配置：超时 3s, 重连 2 次
        self._fault_report_chat = openai.OpenAI(api_key=self._api_key, base_url=self._base_url, timeout=3,
                                                max_retries=2).chat
        self._do_gpt_chat(self._fault_report_chat, get_pre_hot_fault_report(), 'system')

    def _new_advice_chat(self):
        # 预热对话
        # 网络连接配置：超时 3s, 重连 2 次
        self._advice_chat = openai.OpenAI(api_key=self._api_key, base_url=self._base_url, timeout=3, max_retries=2).chat
        self._do_gpt_chat(self._advice_chat, get_pre_hot_suggestion(), 'system')

    def _do_gpt_chat(self, chat, prompt: str, role: str = "user") -> (bool, ChatCompletion):
        """
        -> bool: valid resp
        -> ChatCompletion: ChatCompletion.Choice.message.content := str
        """
        messages = [{"role": role,
                     "content": prompt}]
        return self._do_gpt_chat_from_messages(chat, messages)

    def _do_gpt_chat_from_messages(self, chat, messages) -> (bool, ChatCompletion):
        """
        -> bool: valid resp
        -> ChatCompletion: ChatCompletion.Choice.message.content := str
        """
        # 最大重试次数
        max_retry = 3
        for i in range(max_retry):
            try:
                gpt_response = chat.completions.create(model=self._model_kind,
                                                       messages=messages,
                                                       timeout=20)  # 单次补全超时时间
                if gpt_response:
                    return gpt_response.id is not None, gpt_response
            except openai.APITimeoutError as e:
                logging.error(f"[chatops]: {e}")
                if i < max_retry - 1:
                    # 阻塞时间
                    time.sleep(5)
                else:
                    return False, None
            except openai.RateLimitError as e:
                logging.error(f"[chatops]: {e}")
                return False, None
            except openai.APIStatusError as e:
                logging.error(f"[chatops]: {e}")
                return False, None

    def gpt_update_key(self, api_key: str) -> bool:
        """
        -> False: can't update api_key
        """
        self._api_key: str = api_key
        [getattr(self, method)() for method in dir(self) if
         callable(getattr(self, method)) and re.match(r'_new.*_chat', method)]
        return self.gpt_ping()

    def gpt_change_model(self, new_model: str) -> bool:
        """
        -> False: doesn't find new model
        """
        self._model_kind = new_model
        return self.gpt_ping()

    def gpt_ping(self) -> bool:
        prompt = "hi"
        success, _ = self._do_gpt_chat(self._general_chat, prompt)
        return success

    # 一
    def gen_fault_desc(self, fault_workflow: json, fault_config: json) -> (int, str):
        """
        fault_workflow:
        fault_config:
        """
        _, fault_desc_completion = self._do_gpt_chat(self._fault_desc_chat, get_prompt_fault_desc(fault_workflow))
        if not fault_desc_completion or not fault_desc_completion.choices:
            return 0, None
        fault_desc = fault_desc_completion.choices[0].message.content

        # 将描述写回 redis
        if not app.the_redis:
            print("redis not init")
        fid = app.the_redis.incr('fid')
        app.the_redis.hset('faults', fid, fault_desc)

        return fid, fault_desc

    # 二
    def gen_expect(self, expectation_text: str) -> (int, json):
        """
        expectation_text:
        """
        # todo(cjx): 预处理用户期望文本
        # expectation_text = pre_handle(expectation_text)

        # 将期望写回 redis
        eid = app.the_redis.incr('eid')
        app.the_redis.hset('expectations', eid, expectation_text)

        _, expectation_completion = self._do_gpt_chat(self._expectation_chat, get_prompt_expectation(expectation_text))
        if not expectation_completion or not expectation_completion:
            return 0, None
        expectation = expectation_completion.choices[0].message.content
        return eid, expectation

    # 三
    def gen_fault_result(self, fid: int, fault_play) -> (int, str, str):
        """
        fid: fault id
        -> int: report id
        -> str: report content
        -> str: problem analysis content
        """

        expectation = app.the_redis.hget('expectations', fid)
        if not expectation:
            logging.info("expectation no found")
            expectation = "空"
        else:
            expectation = expectation.decode()

        # 生成 report
        _, fault_report_completion = self._do_gpt_chat_from_messages(self._fault_report_chat,
                                                                     get_messages_fault_report(fault_play,
                                                                                               expectation))
        if not fault_report_completion or not fault_report_completion.choices:
            return 0, None, None

        # 将报告写回 redis
        rid = app.the_redis.incr('rid')
        fault_report = fault_report_completion.choices[0].message.content
        app.the_redis.hset('reports', rid, fault_report)

        # 生成 analysis
        _, fault_analysis_completion = self._do_gpt_chat(self._fault_report_chat, get_prompt_fault_analysis())

        if not fault_analysis_completion or not fault_analysis_completion.choices:
            return 0, None, None

        fault_analysis = fault_analysis_completion.choices[0].message.content

        return rid, fault_report, fault_analysis

    # 四
    def gen_advice(self, fid, rid, eid) -> (int, str):
        """
        fid: fault id
        rid: report id
        eid:

        -> int: advice id
        -> str: advice content
        """
        fault = app.the_redis.hget('faults', fid).decode()
        if not fault:
            logging.error("fault no found")

        if eid == 0:
            expectation = "空"
        else:
            expectation = app.the_redis.hget('expectations', fid).decode()
            if not expectation:
                logging.info("expectation no found")
                expectation = "空"

        report = app.the_redis.hget('reports', rid).decode()
        if not report:
            logging.error("report no found")

        _, advice_completion = self._do_gpt_chat_from_messages(self._fault_report_chat,
                                                               get_messages_suggestion(fault, expectation, report))

        if not advice_completion or not advice_completion.choices:
            return 0, None

        # 将建议写回 redis
        aid = app.the_redis.incr('aid')
        advice = advice_completion.choices[0].message.content
        app.the_redis.hset('reports', aid, advice)

        return aid, advice
