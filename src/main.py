import keyboard
import requests
import smtplib
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()    

def is_iss_overhead(user_lat: float, user_lon: float) -> bool:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    return user_lat - 5 <= iss_latitude <= user_lat + 5 and user_lon - 5 <= iss_longitude <= user_lon + 5


def is_night(user_lat: float, user_lon: float) -> bool:
    parameters = {
        "lat": user_lat,
        "lng": user_lon,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    
    return time_now.hour <= sunrise or time_now.hour >= sunset


def main() -> None:
    lat = float(input("Enter your latitude (Empty or invalid for default): "))
    lon = float(input("Enter your longitude (Empty or invalid for default):"))
    email = input("Enter your email: ")
    print("Entering a loop to send an email when the ISS is overhead! (press q to break)")
    
    while True:
        if keyboard.is_pressed('q'):
            break
        
        if is_iss_overhead(lat, lon) and is_night(lat, lon):
            # Send an email to tell user to look up
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            user_password = os.getenv("USER_PASSWORD", "")
            connection.login(email, user_password)
            connection.sendmail(from_addr=email, to_addrs=email, msg="Look Up!")
        time.sleep(60)
        


if __name__ == "__main__":
    main()