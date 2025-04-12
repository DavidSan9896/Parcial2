FROM python:3.9-slim

WORKDIR /app

COPY analytics_app.py .

RUN pip install pika

CMD ["python", "analytics_app.py"]