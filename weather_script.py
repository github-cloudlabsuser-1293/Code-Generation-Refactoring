import requests

API_KEY = '0ee0f93237fb2afa96daae8235e192d4'  # Replace with your OpenWeatherMap API key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    city = input("Enter city name: ")
    try:
        weather = get_weather(city)
        print(f"Weather in {city}: {weather['weather'][0]['description']}")
        print(f"Temperature: {weather['main']['temp']}°C")
        print(f"Humidity: {weather['main']['humidity']}%")
    except requests.HTTPError as e:
        print("Failed to fetch weather data:", e)