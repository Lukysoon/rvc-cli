FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

RUN git clone  https://github.com/Lukysoon/rvc-cli.git;cd rvc-cli;chmod +x install.sh;./install.sh

EXPOSE 8080
EXPOSE 6006