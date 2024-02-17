FROM python:3.11-alpine

RUN mkdir '/ref_system'

WORKDIR /ref_system

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .