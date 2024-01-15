import smtplib
import os

MY_EMAIL = os.environ["EMAILID"]
PASSWORD = os.environ["PASSWORD"]


class NotificationManager:
    def __init__(self, client, text_message):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=client,
                msg=f"Subject:Flight Deal!!\n\n{text_message}".encode('utf-8')
            )
