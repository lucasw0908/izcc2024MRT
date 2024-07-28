FROM python:3.11.6-alpine3.18 
WORKDIR /app
ADD . /app
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip install uwsgi
EXPOSE 8080
CMD [ "uwsgi", "uwsgi.ini" ]
