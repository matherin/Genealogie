FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
#RUN apt update
#RUN apt install -y libpq-dev python3-dev
RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask","--app","flaskr","run", "--host=0.0.0.0"]
