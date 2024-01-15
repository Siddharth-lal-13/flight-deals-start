import requests
from flight_data import FlightData
import os

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = os.environ["APIKEY"]


class FlightSearch:

    def get_destination_code(self, city_name):
        headers = {
            "apikey": TEQUILA_API_KEY,
        }
        query = {
            "term": city_name,
            "location_types": "city",
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", headers=headers, params=query)
        result = response.json()
        code = result["locations"][0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {
            "apikey": TEQUILA_API_KEY,
        }
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time,
            "date_to": to_time,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "adults": 1,
            "curr": "GBP",
            "max_stopovers": 0,
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=query)

        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=query)

            try:
                data = response.json()["data"][0]
            except IndexError:
                query["max_stopovers"] = 2
                response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=query)

                try:
                    data = response.json()["data"][0]
                except IndexError:
                    print(f"No flights found for {destination_city_code}.")
                    return None
                else:
                    flight_data = FlightData(
                        price=data["price"],
                        origin_city=data["route"][0]["cityFrom"],
                        origin_airport=data["route"][0]["flyFrom"],
                        destination_city=data["route"][2]["cityTo"],
                        destination_airport=data["route"][2]["flyTo"],
                        out_date=data["route"][0]["local_departure"].split("T")[0],
                        return_date=data["route"][3]["local_departure"].split("T")[0],
                        stop_overs=2,
                        via_city=data["route"][0]["cityTo"],
                        via_city2=data["route"][1]["cityTo"],
                        link=data["deep_link"]
                    )
                    print(f"{destination_city_code}: £{flight_data.price}")
                    return flight_data
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"],
                    link=data["deep_link"]
                )
                print(f"{destination_city_code}: £{flight_data.price}")
                return flight_data

        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                link=data["deep_link"]
            )

            print(f"{destination_city_code}: £{flight_data.price}")

            return flight_data
