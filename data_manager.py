import requests
import os

SHEETY_ENDPOINT = os.environ["SHEETY"]


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_user_data(self, first_name, last_name, email):
        new_user = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
            }
        }
        response = requests.post(url=f"{SHEETY_ENDPOINT}/users", json=new_user)
        print(response.text)

    def get_destination_data(self):
        response = requests.get(url=f"{SHEETY_ENDPOINT}/prices")
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_city(self, destination_city):
        new_data = {
            "price": {
                "city": destination_city,
            }
        }
        response = requests.post(url=f"{SHEETY_ENDPOINT}/prices", json=new_data)
        print(response.text)

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }

            response = requests.put(url=f"{SHEETY_ENDPOINT}/prices/{city['id']}", json=new_data)
            print(response.text)

