FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY app ./app

EXPOSE 8000

ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000
ENV APP_RELOAD=false

CMD ["python", "main.py"]