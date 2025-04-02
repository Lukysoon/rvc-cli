#!/bin/bash
mkdir -p datasets

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

mkdir hubert_extra_large
cd hubert_extra_large
wget https://huggingface.co/facebook/hubert-xlarge-ll60k/resolve/main/pytorch_model.bin
wget https://huggingface.co/facebook/hubert-xlarge-ll60k/resolve/main/config.json
cd ..

python3 rvc_cli.py prerequisites

