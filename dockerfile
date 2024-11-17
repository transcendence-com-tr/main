FROM python:3.13-slim

# Çalışma dizini belirle
WORKDIR /app

# requirements.txt dosyasını kopyala ve bağımlılıkları kur
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Django projesini kopyala
COPY . /app/

# Port 8000'i aç
EXPOSE 80
