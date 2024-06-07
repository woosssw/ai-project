FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-devel
# FROM python:3.6-slim-buster

WORKDIR /app

RUN apt-get update

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt-get -y install libgl1-mesa-glx

RUN apt-get -y install libglib2.0-0

RUN pip install -U scikit-learn

RUN pip install -U openmim

RUN pip install -U albumentations

RUN apt-get -y install git

COPY . .

RUN pip install ./flask-uploads

EXPOSE 4000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]