FROM python:3.12-slim

# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Requirements
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Proje dosyaları
COPY . .

# Gunicorn portu
EXPOSE 8000

# Django'yu gunicorn ile başlat
CMD ["gunicorn", "oto_galeri.wsgi:application", "--bind", "0.0.0.0:8000"]
