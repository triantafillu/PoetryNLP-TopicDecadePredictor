# docker run -v C:\Users\alexa\Desktop\Projects\Bootcamp-Repository-Language-2:/tf -it --rm -p 8888:8888 poems_analyzer
# docker build -t poems_analyzer install/ -f install/minimal.Dockerfile
# Details of the base image are here: https://hub.docker.com/r/tensorflow/tensorflow/tags
# It runs Python 3.6

FROM tensorflow/tensorflow:2.3.0-gpu-jupyter

RUN apt-get update && apt-get install -y git
RUN /usr/bin/python3 -m pip install --upgrade pip

RUN mkdir -p /tf
WORKDIR /tf
ENV PYTHONPATH "${PYTHONPATH}:/tf"

COPY ./requirements.txt ./
RUN pip install -r requirements.txt \
  && python3 -m spacy download en_core_web_sm
