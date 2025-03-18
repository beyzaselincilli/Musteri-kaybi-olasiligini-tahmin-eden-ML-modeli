FROM python:3.8-slim

WORKDIR /app

RUN pip install mlflow psycopg2-binary

EXPOSE 5000

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"] 