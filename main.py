from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager
from pprint import pprint

data_manager = DataManager()
flight_search = FlightSearch()
sheet_data = data_manager.get_destination_data()


# User Data
print("\nWelcome to the greatest Flight Club in the World!\n \n        \
We find the best flight deals and email them to you.\n")

first_name = input("What is your first name? ").title()
last_name = input("What is your last name? ").title()

email1 = "email1"
email2 = "email2"

while email1 != email2:
    email1 = input("What's your email? \n")
    if email1.lower() == "exit":
        exit()
    email2 = input("Re-enter your email buddy: \n")
    if email2.lower() == "exit":
        exit()
    if email1 != email2:
        print("\n Tsk. Tsk. Tsk. Buddy, you gotta enter the correct and same email ids both the time..")

print("Congratulations! You are now a part of this premium club!!")
data_manager.get_user_data(first_name=first_name, last_name=last_name, email=email1)


# Flight Data
origin_city = input("Enter the city from where you will begin your journey:\nFROM: ")
origin_city_iata = flight_search.get_destination_code(origin_city)

# destination_city = input("Enter one of your dream destinations:\n ")
# if destination_city not in sheet_data:
#     data_manager.update_destination_city(destination_city=destination_city)
#     sheet_data = data_manager.get_destination_data()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    pprint(f"sheet_data:\n {sheet_data}")

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months_later = tomorrow + timedelta(days=180)


# Flight Booking And Messaging
for destination in sheet_data:
    flight = flight_search.check_flights(
        origin_city_code=origin_city_iata,
        destination_city_code=destination["iataCode"],
        from_time=tomorrow.strftime("%d/%m/%Y"),
        to_time=six_months_later.strftime("%d/%m/%Y")
    )

    if flight is None:
        continue

    if destination["lowestPrice"] > flight.price:
        message = (f"Low Price Alert! Only £{flight.price} to fly from "
                   f"{flight.origin_city}-{flight.origin_airport} to "
                   f"{flight.destination_city}-{flight.destination_airport}, "
                   f"from {flight.out_date} to {flight.return_date}.\n Please head over to the flight booking page "
                   f"via this link: {flight.link}")

        if flight.stop_overs == 1:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        if flight.stop_overs == 2:
            message += f"\nFlight has {flight.stop_overs} stop overs, via {flight.via_city} and {flight.via_city2}."

        NotificationManager(client=email1, text_message=message)

