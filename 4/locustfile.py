from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 2)  # Время ожидания между запросами от 1 до 2 секунд

    @task
    def load_index(self):
        self.client.get("/")  # Тестирование главной страницы

    @task
    def load_inverse(self):
        self.client.post("/inverse", data={"jsonData": '{"key1": "value1", "key2": "value2"}'})  # Тестирование /inverse

    @task
    def load_unstable(self):
        self.client.get("/unstable")  # Тестирование /unstable

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")
