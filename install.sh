#!/bin/bash
mkdir -p datasets

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python3 rvc_cli.py prerequisites