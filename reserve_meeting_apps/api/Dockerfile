FROM python:latest

WORKDIR /var/www/html
COPY requirements.txt ./requirements.txt

RUN apt-get update && \
    apt-get -y install locales vim less && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt
    
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm
