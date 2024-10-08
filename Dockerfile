# Используем базовый образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код приложения в контейнер
COPY . .

# Сделайте скрипт исполняемым
RUN chmod +x /app/start.sh

# Установите точку входа
ENTRYPOINT ["/app/start.sh"]
