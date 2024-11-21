FROM python:3.11-slim

WORKDIR /app

COPY FastApiService/requirements.txt /app/

RUN pip install --default-timeout=100 -r requirements.txt

COPY FastApiService/app /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
