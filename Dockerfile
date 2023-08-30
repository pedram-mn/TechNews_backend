FROM python:3.9.17-alpine3.17
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /technews
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
