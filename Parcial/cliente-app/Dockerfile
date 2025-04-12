FROM python:3.9-slim

WORKDIR /app

COPY cliente_app.py .

RUN pip install flask requests pika

CMD ["python", "cliente_app.py"]