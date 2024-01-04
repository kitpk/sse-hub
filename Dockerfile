FROM python:3.8.16

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Bangkok

RUN apt-get update \
    && apt-get clean \ 
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip  --no-cache-dir

WORKDIR /app
ADD requirements.txt .
ADD .env .
ADD export_env.sh .
RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 8000