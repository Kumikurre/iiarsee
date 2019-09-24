FROM debian:buster

RUN apt-get -y update && apt-get -y install \
   python3-dev \
   python3-pip \
   default-libmysqlclient-dev \
   libcurl4-openssl-dev \
   libssl-dev \
   pkg-config \
   libffi-dev \
   libgirepository1.0-dev \
   libglib2.0 \
   python3-cairo-dev

ADD server.py /
ADD database_init.py /
ADD database_methods.py /

ADD start.sh /

RUN ["chmod", "+x", "/start.sh"]

ADD requirements.txt /

RUN pip3 install -r requirements.txt

