FROM python:3.8-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN \
   apk add libc-dev && \
   apk add alpine-sdk && \
   apk add postgresql-dev && \
   apk add python3-dev && \
   apk add libffi-dev
COPY app .
RUN pip install -U pip
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000