import openai
import re
import logging

from app.config.dev import *
from app.extensions.db import db as redis
from .prompt_manager import *


class GptChatManager:
    def __init__(self, api_key: str = ""):
        """
        api_key: default in env
        """

        if api_key:
            self._api_key = api_key
        else:
            self._api_key = os.environ.get("OPENAI_API_KEY", "")
        assert self._api_key
        self._model_kind = DEFAULT_MODEL

        [getattr(self, method)() for method in dir(self) if
         callable(getattr(self, method)) and re.match(r'_new.*_chat', method)]

    def _new_general_chat(self):
        # 预热普通对话
        # 缺省网络连接配置：超时 3s, 重连 2 次
        self._general_chat = openai.OpenAI(api_key=self._api_key, timeout=3, max_retries=2).chat

    def _new_fault_desc_chat(self):
        # 预热对话
        # 网络连接配置：超时 3s, 重连 2 次
        self._fault_desc_chat = openai.OpenAI(api_key=self._api_key, timeout=3, max_retries=2).chat
        # self._do_gpt_chat(self._fault_desc_chat, self._prompt_manager.build_system_prompt_fault_desc(), "system")

    def _new_expectation_chat(self):
        # 预热对话
        # 网络连接配置：超时 3s, 重连 2 次
        self._expectation_chat = openai.OpenAI(api_key=self._api_key, timeout=3, max_retries=2).chat

    def _new_fault_report_chat(self):
        # 预热对话
        # 网络连接配置：超时 3s, 重连 2 次
        self._fault_report_chat = openai.OpenAI(api_key=self._api_key, timeout=3, max_retries=2).chat
        self._do_gpt_chat(self._fault_report_chat, get_pre_hot_fault_report(), 'system')

    def _new_advice_chat(self):
        # 预热对话
        # 网络连接配置：超时 3s, 重连 2 次
        self._advice_chat = openai.OpenAI(api_key=self._api_key, timeout=3, max_retries=2).chat
        self._do_gpt_chat(self._advice_chat, get_pre_hot_suggestion(), 'system')

    def _do_gpt_chat(self, chat, prompt: str, role: str = "user") -> (bool, json):
        try:
            gpt_response = chat.completions.create(model=self._model_kind,
                                                   messages=[{"role": role,
                                                              "content": prompt}])
        except openai.APITimeoutError as e:
            logging.error(f"[chatops]: {e}")
            return False, None
        except openai.RateLimitError as e:
            logging.error(f"[chatops]: {e}")
            return False, None
        except openai.APIStatusError as e:
            logging.error(f"[chatops]: {e}")
            return False, None

        return gpt_response.id is not None, gpt_response

    def _do_gpt_chat_from_messages(self, chat, messages) -> (bool, json):
        try:
            gpt_response = chat.completions.create(model=self._model_kind,
                                                   messages=messages)
        except openai.APITimeoutError as e:
            logging.error(f"[chatops]: {e}")
            return False, None
        except openai.RateLimitError as e:
            logging.error(f"[chatops]: {e}")
            return False, None
        except openai.APIStatusError as e:
            logging.error(f"[chatops]: {e}")
            return False, None

        return gpt_response.id is not None, gpt_response

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

    def gen_fault_desc(self) -> bool:
        # todo(xla)
        pass

    def gen_expect(self) -> bool:
        # todo(xla)
        pass

    def gen_fault_report(self, fid) -> (int, json):
        """
        fid: fault id
        """
        fault = redis.hget('faults', fid)
        if not fault:
            logging.error("fault no found")

        expectation = redis.hget('expectations', fid)
        if not expectation:
            logging.error("expectation no found")

        _, fault_report = self._do_gpt_chat_from_messages(self._fault_report_chat,
                                                          messages=get_messages_summary_fault_report(fault,
                                                                                                     expectation))

        if not fault_report:
            return 0, None

        # 将报告写回 redis
        redis['rid'] += 1
        rid = redis['rid']
        redis.hset('reports', rid, fault_report)

        return rid, fault_report

    def gen_advice(self, fid) -> (int, json):
        """
                fid: fault id
                """
        fault = redis.hget('faults', fid)
        if not fault:
            logging.error("fault no found")

        expectation = redis.hget('expectations', fid)
        if not expectation:
            logging.error("expectation no found")

        report = redis.hget('reports', fid)
        if not report:
            logging.error("report no found")

        _, advice = self._do_gpt_chat_from_messages(self._fault_report_chat,
                                                    messages=get_messages_suggestion(fault, expectation, report))

        if not advice:
            return 0, None

        # 将建议写回 redis
        redis['aid'] += 1
        aid = redis['aid']
        redis.hset('reports', aid, advice)

        return aid, advice
