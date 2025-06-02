import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io

def fetch_weather(city, api_key):
    # First, get lat/lon for the city
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    city_data = response.json()
    lat = city_data['coord']['lat']
    lon = city_data['coord']['lon']

    # Now, use One Call 2.5 API (free tier)
    onecall_url = "https://api.openweathermap.org/data/2.5/onecall"
    onecall_params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,daily,alerts",
        "appid": api_key,
        "units": "metric"
    }
    onecall_resp = requests.get(onecall_url, params=onecall_params)
    onecall_resp.raise_for_status()
    weather_data = onecall_resp.json()

    # Attach city name and weather description for display
    weather_data['city_name'] = city_data['name']
    weather_data['weather'] = city_data['weather']
    return weather_data

def get_icon(icon_code):
    url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(url)
    img_data = response.content
    return Image.open(io.BytesIO(img_data))

class WeatherDashboard(tk.Tk):
    def __init__(self, api_key):
        super().__init__()
        self.title("Weather Dashboard")
        self.geometry("400x350")
        self.api_key = api_key

        self.city_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        ttk.Label(frame, text="Enter city name:").grid(row=0, column=0, padx=5)
        city_entry = ttk.Entry(frame, textvariable=self.city_var)
        city_entry.grid(row=0, column=1, padx=5)
        city_entry.bind("<Return>", lambda e: self.show_weather())

        search_btn = ttk.Button(frame, text="Search", command=self.show_weather)
        search_btn.grid(row=0, column=2, padx=5)

        self.card_frame = ttk.Frame(self, relief="raised", borderwidth=2)
        self.card_frame.pack(pady=20, fill="x", padx=20)

        self.icon_label = ttk.Label(self.card_frame)
        self.icon_label.grid(row=0, column=0, rowspan=2, padx=10)

        self.desc_label = ttk.Label(self.card_frame, font=("Arial", 14))
        self.desc_label.grid(row=0, column=1, sticky="w")

        self.temp_label = ttk.Label(self.card_frame, font=("Arial", 12))
        self.temp_label.grid(row=1, column=1, sticky="w")

        self.humidity_label = ttk.Label(self.card_frame, font=("Arial", 12))
        self.humidity_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.wind_label = ttk.Label(self.card_frame, font=("Arial", 12))
        self.wind_label.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    def show_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
        try:
            data = fetch_weather(city, self.api_key)
            icon_code = data['weather'][0]['icon']
            icon_img = get_icon(icon_code)
            icon_img = icon_img.resize((64, 64), Image.ANTIALIAS)
            self.tk_icon = ImageTk.PhotoImage(icon_img)
            self.icon_label.config(image=self.tk_icon)

            desc = data['weather'][0]['description'].capitalize()
            temp = data['current']['temp']
            humidity = data['current']['humidity']
            wind = data['current']['wind_speed']

            self.desc_label.config(text=f"{desc}")
            self.temp_label.config(text=f"Temperature: {temp}°C")
            self.humidity_label.config(text=f"Humidity: {humidity}%")
            self.wind_label.config(text=f"Wind: {wind} m/s")
        except requests.HTTPError as e:
            messagebox.showerror("Error", f"Failed to fetch weather data:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    # Replace with your valid OpenWeatherMap API key
    API_KEY = "1adab69a4f50dc065165cb1f609fc397"
    app = WeatherDashboard(API_KEY)
    app.mainloop()
