# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Устанавливаем переменные окружения (если нужно)
ENV PYTHONUNBUFFERED=1

# Запуск main.py
CMD ["python", "main.py"]