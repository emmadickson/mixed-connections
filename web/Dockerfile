FROM python:3.9

WORKDIR /project
ADD . /project

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uwsgi", "app.ini"]
