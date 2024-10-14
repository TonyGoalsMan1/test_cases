import pytest
from server_simple import app

@pytest.fixture
def client():
    """
    Фикстура для создания тестового клиента Flask
    """
    with app.test_client() as client:
        yield client

def test_inverse_success(client):
    """
    Тест успешного запроса на маршрут /inverse
    """
    response = client.post('/inverse', data={'jsonData': '{"key1": "value1", "key2": "value2"}'})
    assert response.status_code == 200
    assert response.get_json() == {"value1": "key1", "value2": "key2"}

def test_inverse_invalid_json(client):
    """
    Тест, если переданы некорректные данные
    """
    response = client.post('/inverse', data={'jsonData': 'invalid_json'})
    assert response.status_code == 400
    assert response.is_json  # Проверяем, что ответ в формате JSON
    assert response.get_json() == {"error": "Ошибка обработки JSON"}

def test_inverse_not_dict(client):
    """
    Тест, если передан JSON, который не является объектом
    """
    response = client.post('/inverse', data={'jsonData': '["list_item1", "list_item2"]'})
    assert response.status_code == 400
    assert response.is_json  # Проверяем, что ответ в формате JSON
    assert response.get_json() == {"error": "Тело запроса должно быть JSON-объектом"}

def test_unstable(client):
    """
    Тест для маршрута /unstable
    """
    response = client.get('/unstable')
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.get_json() == {"message": "HAPPY"}
    elif response.status_code == 400:
        assert response.get_json() == {"message": "UNHAPPY"}

def test_inverse_empty_data(client):
    """
    Тест, если данные не переданы (пустое тело запроса)
    """
    response = client.post('/inverse', data={})
    assert response.status_code == 400
    assert response.is_json  # Проверяем, что ответ в формате JSON
    assert response.get_json() == {"error": "Ошибка обработки JSON"}

def test_inverse_invalid_method(client):
    """
    Тест, если выполнен недопустимый метод запроса (GET вместо POST на /inverse)
    """
    response = client.get('/inverse')
    assert response.status_code == 405  # Метод не разрешен (Method Not Allowed)

def test_swagger_apidocs(client):
    """
    Тест, что Swagger-документация доступна по маршруту /apidocs
    """
    response = client.get('/apidocs')
    assert response.status_code == 200  # Страница Swagger должна успешно загрузиться
    assert "Swagger UI" in response.get_data(as_text=True)  # Проверяем, что в ответе есть Swagger UI

def test_unstable_multiple_requests(client):
    """
    Тест для многократных запросов на маршрут /unstable
    Проверяем, что могут возвращаться как 200, так и 400 статусы
    """
    has_happy = False
    has_unhappy = False

    for _ in range(10):
        response = client.get('/unstable')
        if response.status_code == 200:
            has_happy = True
            assert response.get_json() == {"message": "HAPPY"}
        elif response.status_code == 400:
            has_unhappy = True
            assert response.get_json() == {"message": "UNHAPPY"}

    assert has_happy, "Не было получено ни одного статуса 200"
    assert has_unhappy, "Не было получено ни одного статуса 400"


