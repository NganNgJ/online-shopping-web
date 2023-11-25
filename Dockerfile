FROM python:3.7.5

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app

EXPOSE 8000

RUN pip install -r requirements.txt

RUN pip install channels
RUN pip install channels-redis

RUN groupadd --gid 1000 ngan
RUN useradd -u 1000 ngan -g ngan --home /app
RUN chown -R ngan:ngan /app
USER ngan


CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
