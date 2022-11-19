from locust import HttpUser, task
import random
import time
post_headers={'content-type':'application/x-www-form-urlencoded'}
class LiverPrediction(HttpUser):
    @task
    def predict_page(self):
        self.client.get('/prediction_form')
    @task(20)
    def predict(self):
        self.client.get('/predict')
