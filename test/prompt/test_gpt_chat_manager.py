import os
import pytest
from app.prompt.gpt_chat_manager import GptChatManager


@pytest.fixture
def the_chat_manager():
    # 单测要传入 api_key
    return GptChatManager()


def test_ping(the_chat_manager):
    assert the_chat_manager.gpt_ping()


def test_ping_with_invalid_api_key(the_chat_manager):
    the_chat_manager.gpt_update_key("invalid_api_key")
    assert not the_chat_manager.gpt_ping()


def test_ping_with_broken_network():
    os.environ["http_proxy"] = ""
    os.environ["https_proxy"] = ""
    the_chat_manager = GptChatManager()
    # todo(fxc): 应该在 3*3s 内结束，但实际上 21 s。
    assert not the_chat_manager.gpt_ping()
