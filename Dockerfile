FROM python:3.11

RUN mkdir /auth_app

WORKDIR /auth_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
