FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN pip freeze > requirements.txt
COPY . /app

