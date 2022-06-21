FROM python:3.8

WORKDIR session

COPY requirement.txt

RUN pip install -r requirement.txt

COPY . . .

CMD ['nameko run service']

CMD ['nameko run news_service']