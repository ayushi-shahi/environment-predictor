import os
import requests
import pandas as pd
from dotenv import load_dotenv
import json
from datetime import datetime
import time

# Load API keys from .env
load_dotenv()
OPENWEATHER_API_KEY = "OWM_API_KEY"  # Replace with your actual OpenWeather API key
BREEZO_API_KEY = "BREEZO_API_KEY"  # Replace with your actual Google API key

# Expanded list of cities (300 cities including 100 from India and 200 international)
CITIES = [
    # International Cities
    "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Jaipur", "Ahmedabad", "Lucknow",
    "London", "New York", "Tokyo", "Sydney", "Los Angeles", "Paris", "Berlin", "Dubai", "Rome", "Istanbul",
    "Shanghai", "Beijing", "Bangkok", "Singapore", "Seoul", "Jakarta", "Toronto", "San Francisco", "Hong Kong",
    "Moscow", "Cairo", "Lagos", "Mexico City", "Sao Paulo", "Rio de Janeiro", "Buenos Aires", "Vancouver", 
    "Kuala Lumpur", "Melbourne", "Austin", "Atlanta", "Dallas", "Seattle", "Philadelphia", "Denver", "Miami",
    "Manila", "Bucharest", "Warsaw", "Lisbon", "Prague", "Budapest", "Stockholm", "Copenhagen", "Oslo", "Helsinki", 
    "Brussels", "Athens", "Lagos", "Riyadh", "San Diego", "Portland", "Montreal", "Cape Town", "Abu Dhabi", "Lima",
    "Cartagena", "Kigali", "Doha", "Tel Aviv", "Vancouver", "Bordeaux", "Bologna", "Luxembourg", "Vilnius", "Helsinki",
    "Madrid", "Zurich", "Vienna", "London", "Berlin", "Paris", "Barcelona", "Bangkok", "Singapore", "Brussels", "Munich",
    "San Jose", "Montreal", "Athens", "Los Angeles", "Madrid", "Mexico City", "Seattle", "Vancouver", "Lima", "Sydney",
    "Johannesburg", "Mumbai", "Karachi", "Nagoya", "Jakarta", "Istanbul", "Paris", "San Juan", "Copenhagen", "Lagos",
    "Port-au-Prince", "Vientiane", "Baku", "Cairo", "Lima", "Kinshasa", "Seoul", "Addis Ababa", "Paris", "Jakarta", "Bangalore",
    "Hong Kong", "Mexico City", "Guangzhou", "Taipei", "Dhaka", "Islamabad", "Abu Dhabi", "Singapore", "Manila", "Moscow",
    "Karachi", "Nagoya", "Jakarta", "Istanbul", "Paris", "Santiago", "Kinshasa", "Quito", "Gustavo", "Nairobi", "Lima",
    "Kolkata", "Shanghai", "Brussels", "Rome", "Madrid", "Melbourne", "Munich", "Copenhagen", "Manila", "Monaco", "Santiago",
    "Madrid", "Vienna", "Lima", "Brisbane", "Vancouver", "Sao Paulo", "Karachi", "Guangzhou", "Lagos", "Yerevan", "Lima",
    "Tirana", "Wroclaw", "Pittsburgh", "Santiago", "Dublin", "Dallas", "Sydney", "Hong Kong", "Moscow", "Hong Kong", "Dubai",
    "Atlanta", "Houston", "Chicago", "Colombo", "Munich", "Salvador", "Vilnius", "Lagos", "Adelaide", "Brisbane", "Rio",
    "Mexico City", "Rio", "Budapest", "Cape Town", "Kigali", "San Salvador", "Minsk", "Montpellier", "Vienna", "Porto",
    "Belgrade", "Skopje", "Doha", "Nairobi", 

    # Additional Cities from India
    "Agra", "Ajmer", "Aligarh", "Ambala", "Amritsar", "Anantapur", "Aurangabad", "Bhopal", "Bilaspur", "Bokaro",
    "Chandigarh", "Chennai", "Coimbatore", "Dehradun", "Dhanbad", "Gandhinagar", "Ghaziabad", "Gorakhpur", "Guwahati", "Hubli",
    "Indore", "Jabalpur", "Jammu", "Jamshedpur", "Jodhpur", "Kanpur", "Kochi", "Kolkata", "Kolkata", "Kota", "Lucknow", 
    "Ludhiana", "Madurai", "Malappuram", "Mangalore", "Meerut", "Moradabad", "Mumbai", "Muzaffarpur", "Nagpur", "Nashik",
    "Navi Mumbai", "Patna", "Pondicherry", "Raipur", "Rajkot", "Ranchi", "Shimla", "Surat", "Srinagar", "Thane", "Tirupati",
    "Trichy", "Udaipur", "Vadodara", "Varanasi", "Vijayawada", "Visakhapatnam", "Agartala", "Aurangabad", "Bhubaneswar",
    "Chandrapur", "Faridabad", "Haldwani", "Hassan", "Jalgaon", "Jammu", "Kurnool", "Mysuru", "Nellore", "Panipat", "Ranchi",
    "Rewari", "Satna", "Shimla", "Sonipat", "Surat", "Ujjain", "Zirakpur"
]


# Mock function for air quality forecasting (use your actual model here)
def forecast_aqi(current_aqi):
    return current_aqi  # Replace with actual forecast logic

# Health Recommendations based on AQI
def health_advisory(aqi):
    if aqi <= 50:
        return "Outdoor activities are safe for everyone."
    elif aqi <= 100:
        return "Sensitive groups should limit prolonged outdoor activities."
    elif aqi <= 150:
        return "People with respiratory conditions should avoid outdoor activities."
    else:
        return "Everyone should avoid outdoor activities due to unhealthy air quality."

# Pollution alert logic (mock example)
def pollution_alert(aqi, dominant_pollutant):
    if aqi > 150:
        return f"Alert: High pollution levels detected due to {dominant_pollutant}."
    return "Pollution levels are within safe limits."

# Process each city
all_data = []

for CITY in CITIES:
    # Get coordinates of the city using OpenWeather API
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
    weather_res = requests.get(weather_url).json()

    if "coord" not in weather_res:
        print(f"Error: {weather_res.get('message', 'Unknown error occurred while fetching weather data')} for {CITY}")
        continue
    
    lat = weather_res["coord"]["lat"]
    lon = weather_res["coord"]["lon"]
    
    print(f"Coordinates for {CITY}: Latitude = {lat}, Longitude = {lon}")
    
    # Get air quality data using Breezometer API
    air_quality_url = f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={BREEZO_API_KEY}"
    payload = {"location": {"latitude": lat, "longitude": lon}}
    headers = {'Content-Type': 'application/json'}
    air_quality_res = requests.post(air_quality_url, headers=headers, data=json.dumps(payload))
    
    if air_quality_res.status_code == 200:
        data = air_quality_res.json()
        aqi = data['indexes'][0]['aqi']
        dominant_pollutant = data['indexes'][0]['dominantPollutant']
        predicted_aqi = forecast_aqi(aqi)
        advisory = health_advisory(aqi)
        alert = pollution_alert(aqi, dominant_pollutant)
        
        combined = {
            "city": CITY,
            "latitude": lat,
            "longitude": lon,
            "temperature": weather_res["main"]["temp"],
            "humidity": weather_res["main"]["humidity"],
            "wind_speed": weather_res["wind"]["speed"],
            "weather_description": weather_res["weather"][0]["description"],
            "air_quality_index": aqi,
            "predicted_aqi": predicted_aqi,
            "category": data['indexes'][0]['category'],
            "dominant_pollutant": dominant_pollutant,
            "health_advisory": advisory,
            "pollution_alert": alert,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        all_data.append(combined)
    else:
        print(f"Error fetching air quality data: {air_quality_res.status_code} - {air_quality_res.text}")

    # Delay
time.sleep(1)
df = pd.DataFrame(all_data)

# Save the combined data into a CSV file
df.to_csv("environment_data.csv", index=False)

print("CSV file has been saved successfully.")