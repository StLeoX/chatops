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

        self._general_chat: openai.Client.chat
        self._fault_desc_chat: openai.Client.chat
        self._expectation_chat: openai.Client.chat
        self._fault_report_chat: openai.Client.chat
        self._advice_chat: openai.Client.chat
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
        self._do_gpt_chat(self._fault_desc_chat, get_pre_hot_fault_desc(), 'system')

    def _new_expectation_chat(self):
        # 预热对话
        # 网络连接配置：超时 3s, 重连 2 次
        self._expectation_chat = openai.OpenAI(api_key=self._api_key, timeout=3, max_retries=2).chat
        self._do_gpt_chat(self._expectation_chat, get_pre_hot_expectation(), 'system')

    def _new_fault_report_chat(self):
        # 预热对话
        # 网络连接配置：超时 3s, 重连 2 次
        self._fault_report_chat = openai.OpenAI(api_key=self._api_key, timeout=3, max_retries=2).chat

    def _new_advice_chat(self):
        # 预热对话
        # 网络连接配置：超时 3s, 重连 2 次
        self._advice_chat = openai.OpenAI(api_key=self._api_key, timeout=3, max_retries=2).chat

    def _do_gpt_chat(self, chat: openai.Client.chat, prompt: str, role: str = "user") -> bool:
        try:
            response = chat.completions.create(model=self._model_kind,
                                               messages=[{"role": role,
                                                          "content": prompt}])
        except openai.APITimeoutError as e:
            logging.error(f"[chatops]: {e}")
            return False
        except openai.RateLimitError as e:
            logging.error(f"[chatops]: {e}")
            return False
        except openai.APIStatusError as e:
            logging.error(f"[chatops]: {e}")
            return False

        return response.id is not None

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
        hi = "hi"
        prompt = self._prompt_manager.build_prompt_dummy(hi)
        return self._do_gpt_chat(self._general_chat, prompt)

    def gen_fault_desc(self, fault_workflow: json, fault_config: json) -> (int, str):
        """
        fault_workflow:
        fault_config:
        """
        _, fault_desc = self._do_gpt_chat(self._fault_desc_chat, get_prompt_fault_desc(fault_workflow))
        if not fault_desc:
            return 0, None

        # 将描述写回 redis
        redis['fid'] += 1
        fid = redis['fid']
        redis.hset('faults', fid, fault_desc)

        return fid, fault_desc

    def gen_expect(self, expectation_text: str) -> (int, json):
        """
        expectation_text:
        """
        # todo(cjx): 预处理用户期望文本
        # expectation_text = pre_handle(expectation_text)

        # 将期望写回 redis
        redis['eid'] += 1
        eid = redis['eid']
        redis.hset('expectations', eid, expectation_text)

        _, expectation_json = self._do_gpt_chat(self._expectation_chat, get_prompt_expectation(expectation_text))
        if not expectation_json:
            return 0, None

        return eid, expectation_json
