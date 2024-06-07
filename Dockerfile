FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-devel

WORKDIR /app

RUN apt-get update

RUN apt-get -y install git

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]