@echo off

REM Переход в директорию проекта
cd C:\MTS\pythonProject

REM Активируем виртуальную среду
call .venv\Scripts\activate

REM Устанавливаем переменную окружения FLASK_APP
set FLASK_APP=3\server_simple.py

REM Запуск Flask сервера в фоновом режиме
start /B flask run

REM Ожидание запуска сервера
timeout /t 5

REM Мониторинг CPU и RAM каждые 10 секунд
:monitor
    echo ================================
    echo Monitoring CPU Load:
    wmic cpu get loadpercentage
    echo Monitoring Free RAM:
    wmic OS get FreePhysicalMemory /Value
    timeout /t 10
    goto monitor

REM Запуск Locust
locust -f 4\locustfile.py --headless -u 10 -r 2 -t 1m --host=http://127.0.0.1:5000

REM Остановка сервера Flask
taskkill /F /IM flask.exe
