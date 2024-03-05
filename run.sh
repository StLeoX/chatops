#!/bin/bash
export FLASK_DEBUG="False"; \
export BASE_URL="https://openai.ehco-relay.cc/v1/"; \
export OPENAI_API_KEY="sk-oGUKnIjOcmTBspSfB01fC2E8D24f485c8f45E361Ae5aCfBd"; \
export REDIS_URL="redis://172.17.0.2:6379/0"; \
./venv/bin/python -m gunicorn --bind 0.0.0.0:9999 server:app --timeout 120