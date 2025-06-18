from locust import HttpUser, task


class User(HttpUser):
    # wait_time = between(1, 5)

    # @task
    # def hello_world(self):
    #     self.client.get("/analysis/AFLT_final/forecast")

    @task
    def hello_world(self):
        self.client.get("/analysis/AFLT_final/forecastsync")

    # @task
    # def hello_world(self):
    #     self.client.get("/analysis/hello/sync")

    # def on_start(self):
    #     self.client.post("/login", json={"login": "user1", "password": "qwerty"})
