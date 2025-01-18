#!/bin/bash
mkdir -p datasets
mkdir -p pretrained

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python3 -m ipykernel install --user --name=venv

python3 rvc_cli.py prerequisites