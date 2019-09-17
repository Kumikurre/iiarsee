FROM python:3

ADD server.py /
ADD database_init.py /
ADD database_methods.py /

ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "-u", "./server.py" ]