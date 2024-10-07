# Используем базовый образ с Python 3.9
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порт (если бот использует вебхуки или веб-сервер, например)
# EXPOSE 8000  # Откройте порт, если нужно

# Команда для запуска бота
CMD ["python", "run.py"]
