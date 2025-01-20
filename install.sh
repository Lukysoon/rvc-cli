pip install --upgrade pip

# create base directories
mkdir -p datasets
mkdir -p pretrained

# create and activate virtual env
python3 -m venv venv
source venv/bin/activate

# install necessary libraries

# install jupyter kernel to virtual environment 
pip install ipykernel
python3 -m ipykernel install --user --name=venv

apt update
apt install ffmpeg

pip install -r requirements.txt

python3 rvc_cli.py prerequisites