#!/bin/sh

# Выполняем миграции
echo "Running migrations..."
python manage.py migrate

# Проверка наличия файла, который будет создан после первого запуска csu
if [ ! -f /app/csu_done ]; then
    echo "Running csu..."
    python manage.py csu
    touch /app/csu_done  # Создаем файл, чтобы обозначить, что команда уже была выполнена
else
    echo "csu has already been run."
fi

# Запускаем сервер
echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000