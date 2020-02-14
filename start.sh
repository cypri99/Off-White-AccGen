#!/bin/bash
set -e # Makes script crash upon error

pip install -r requirements.txt
python3 main.py
