import os
import requests
import schedule
import time
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

CITY = "Galle" 
COUNTRY_CODE = "LK" 

IMAGE_PATH = os.path.abspath("./weather_wallpaper.jpg")

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY_CODE}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_desc = data['weather'][0]['main'].lower()  
        print(f"Current Weather: {weather_desc}")
        return weather_desc
    else:
        print("Error fetching weather:", data)
        return None

def download_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&orientation=landscape&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    data = response.json()
    print(data)

    if "urls" in data:
        image_url = data["urls"]["full"]
        img_data = requests.get(image_url).content
        with open(IMAGE_PATH, "wb") as handler:
            handler.write(img_data)
        print(f"Downloaded wallpaper for {query}.")
    else:
        print("Error fetching image from Unsplash:", data)

def set_wallpaper():
    cmd_light = f"gsettings set org.gnome.desktop.background picture-uri file://{IMAGE_PATH}"
    cmd_dark = f"gsettings set org.gnome.desktop.background picture-uri-dark file://{IMAGE_PATH}"
    os.system(cmd_light)
    os.system(cmd_dark)

def update_wallpaper():
    weather = get_weather()
    if weather:
        download_image(weather)
        set_wallpaper()

schedule.every(1).minutes.do(update_wallpaper)

print("Weather wallpaper updater running... ")
while True:
    schedule.run_pending()
    time.sleep(30)  
