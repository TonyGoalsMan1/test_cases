from flask import Flask, request, jsonify, render_template_string
from flasgger import Swagger
import random
import json

app = Flask(__name__)
swagger = Swagger(app)

# Шаблон HTML для главной страницы
html_template = '''
<html>
    <body>
        <h1>Добро пожаловать на наш сервер!</h1>
        <p>Отправить запрос на <code>/inverse</code>:</p>
        <form action="/inverse" method="post">
            <textarea name="jsonData" rows="4" cols="50" placeholder='{"key1": "value1", "key2": "value2"}'></textarea><br>
            <button type="submit">Отправить</button>
        </form>
        <p><a href="/unstable">Перейти на /unstable</a></p>
        <p><a href="/apidocs">Перейти к документации API (Swagger)</a></p>
    </body>
</html>
'''

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template_string(html_template)

# Маршрут /inverse для POST-запросов
@app.route('/inverse', methods=['POST'])
def inverse():
    """
    Инвертирует ключи и значения в JSON-объекте.
    ---
    parameters:
      - name: jsonData
        in: formData
        type: string
        required: true
        description: JSON-объект для инверсии.
    responses:
      200:
        description: Успешно инвертированный JSON-объект.
      400:
        description: Ошибка обработки JSON.
    """
    try:
        json_data = request.form['jsonData']
        data = json.loads(json_data)

        if not isinstance(data, dict):
            return jsonify({"error": "Тело запроса должно быть JSON-объектом"}), 400

        inverted_data = {v: k for k, v in data.items()}
        return jsonify(inverted_data), 200  # Возвращаем JSON, а не HTML
    except (json.JSONDecodeError, TypeError):
        return jsonify({"error": "Ошибка обработки JSON"}), 400  # Возвращаем JSON при ошибке

# Маршрут /unstable для GET-запросов
@app.route('/unstable', methods=['GET'])
def unstable():
    """
    Возвращает случайное сообщение.
    ---
    responses:
      200:
        description: HAPPY
      400:
        description: UNHAPPY
    """
    if random.choice([True, False]):
        return jsonify({"message": "HAPPY"}), 200
    else:
        return jsonify({"message": "UNHAPPY"}), 400

if __name__ == '__main__':
    app.run()
