#!/bin/bash

#Создаем виртуальную среду, если не создана
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi


source .venv/bin/activate

#Установка зависимостей
pip install -r 3/requirements.txt

export FLASK_APP=3/server_simple.py

#Запуск Flask сервера в фоновом режиме
flask run &

#Ожидание запуска сервера
sleep 5

# Запуск Locust для нагрузочного тестирования
locust -f 4/locustfile.py --headless -u 10 -r 2 -t 1m --host=http://127.0.0.1:5000

pkill -f flask

deactivate
