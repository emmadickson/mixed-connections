FROM python:3.6.1-alpine

WORKDIR /project
ADD . /project
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add jpeg-dev zlib-dev libjpeg
RUN apk add  linux-headers pcre-dev
RUN pip install -r requirements.txt
EXPOSE 5000

CMD ["uwsgi", "app.ini"]
