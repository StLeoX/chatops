#!/bin/bash
./venv/bin/python -m gunicorn --bind 0.0.0.0:9999 server:app