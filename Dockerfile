# используем минимальный образ Python
FROM python:3.11-slim

# устанавливаем рабочую директорию в контейнере
WORKDIR /app

# копируем файл зависимостей
COPY requirements.txt .

# устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# копируем всю остальную папку внутрь контейнера
COPY . .

# устанаавливаем переменные окружения для Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# открываем порт 5000, где работает Flask
EXPOSE 5000

# команда запуска по умолчанию
CMD ["flask", "run"]
