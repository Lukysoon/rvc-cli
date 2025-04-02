#!/bin/bash
mkdir -p datasets

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

mkdir hubert_large
cd hubert_large
wget https://huggingface.co/facebook/hubert-large-ls960-ft/resolve/main/pytorch_model.bin
wget https://huggingface.co/facebook/hubert-large-ls960-ft/resolve/main/config.json
cd ..

python3 rvc_cli.py prerequisites

