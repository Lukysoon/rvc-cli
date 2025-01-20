
# create base directories
mkdir -p datasets
mkdir -p pretrained

# create and activate virtual env
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip

# install jupyter kernel to virtual environment 
pip install ipykernel
python3 -m ipykernel install --user --name=venv

apt update
apt install ffmpeg -y

pip install -r requirements.txt

python3 rvc_cli.py prerequisites