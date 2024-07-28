FROM python:3.11.6-alpine3.18 
WORKDIR /app
ADD . /app
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
CMD [ "uwsgi", "uwsgi.ini" ]
