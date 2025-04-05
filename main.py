import requests
import os
from dotenv import load_dotenv
import pandas as pd

# Load .env variables
load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")
CITY = "Delhi"

# API call
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
response = requests.get(url)
data = response.json()

# Extract and show info
weather = {
    "city": data["name"],
    "temperature": data["main"]["temp"],
    "humidity": data["main"]["humidity"],
    "wind_speed": data["wind"]["speed"],
    "description": data["weather"][0]["description"]
}

df = pd.DataFrame([weather])
print(df)
