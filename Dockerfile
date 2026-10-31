# Беремо офіційний базовий образ Python
FROM python:3.12-slim

# Забороняємо Python писати файли .pyc на диск і вмикаємо миттєвий вивід логів
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Створюємо робочу папку всередині контейнера
WORKDIR /app

# Спочатку копіюємо requirements і ставимо залежності (це кешується Docker)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь наш проєкт у контейнер
COPY . /app/