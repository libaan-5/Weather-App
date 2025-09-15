import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import requests
import json
from dotenv import load_dotenv
import os

# Read environment variables from .env (used for storing API credentials securely)
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


# Function used to locate the 'weather' directory 
def find_subdirectory(target_dir_name):
    current_dir = os.getcwd()
    for item in os.listdir(current_dir):
        full_path = os.path.join(current_dir, item)
        if os.path.isdir(full_path) and item == target_dir_name:
            return full_path
    return None

class MyGUI:

    def __init__(self):

        self.root = tk.Tk()   # store in self
        self.root.title("Weather App")

        # Customize the window size here (width x height)
        self.root.geometry("300x320") 

        # Input field
        self.entry = ttk.Entry(self.root, width=40)  # store in self
        self.entry.pack(pady=30)

        # Button to submit input
        button = ttk.Button(self.root, text="Submit", command=self.submit)
        button.pack()

        # Output label (empty at start)
        self.output_label = tk.Label(self.root, text="", font=('Arial', 12))
        self.output_label.pack(pady=10)

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Handle error responses
        self.error_messages = {
            400: "Error 400: Bad request (maybe missing parameters or invalid query).",
            401: "Error 401: Invalid API key.",
            404: "Error 404: City not found (incorrect input).",
            429: "Error 429: Too many requests – you’ve hit the API limit."
        }

        self.weather_types = ["Clear", "Clouds", "Rain", "Snow", "Thunderstorm", "Haze"]

        self.found_path = find_subdirectory("weather")

        self.root.mainloop()

    def clear_image(self):
        self.image_label.config(image="")
        self.image_label.image = None

    def get_weather(self, city, country_code=None, units=None): 
            params = {
                "q": f"{city},{country_code}" if country_code else city,
                "appid": API_KEY,
                "units": units  # Celsius
            }
            response = requests.get(BASE_URL, params=params)
            
            # If the input was valid and everything went well
            if response.status_code == 200:
                data = response.json()

               # .get() has defaults (fallbacks) so missing fields (e.g., no "country") won’t raise KeyError
                name = data.get("name", "Unknown")
                country = data.get("sys", {}).get("country", "N/A")
                temp = data.get("main", {}).get("temp", "??")
                self.simple_weather = data.get("weather", [{}])[0].get("main", "Unknown")
                weather = data.get("weather", [{}])[0].get("description", "Unknown")

                unit_symbol = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
                output_weather = f"Country: {country},\n Weather in {name}: {weather},\n Temperature: {temp}{unit_symbol}\n"

                return output_weather
            
            return self.error_messages.get(
                response.status_code,
                # fallback code if status code not found in above dictionary
                f"Error {response.status_code}: Unexpected API error." 
            )

        
    # --------------------------
    # Function called when button is clicked
    # --------------------------
    def submit(self):

        user_input = self.entry.get().strip() # Eliminates white-space (before or after input)

        parts = [p.strip() for p in user_input.split(",")]

        city = parts[0]
        country_code = None
        units = "metric"  # default Celsius

        symbols = {'C': 'metric', 'F': 'imperial', 'K': None}

        if len(parts) >= 2:
            if parts[1] in symbols:
                units = symbols[parts[1]]
            else:
                country_code = parts[1]

        if len(parts) >= 3 and parts[2] in symbols:
            units = symbols[parts[2]]

        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye! 👋")
            self.root.destroy()
        elif user_input:
            weather_text = self.get_weather(city, country_code, units)
            self.output_label.config(text=weather_text)
            self.entry.delete(0, tk.END)

            if weather_text not in self.error_messages.values():
                if self.simple_weather in self.weather_types and self.found_path:
                    image_path = os.path.join(self.found_path, f"{self.simple_weather}.png")
                    try:
                        img = Image.open(image_path)
                        img = img.resize((100, 100), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)

                        self.image_label.config(image=photo)
                        self.image_label.image = photo
                    except FileNotFoundError:
                        # Clear image if file not found
                        self.clear_image()
                else:
                    # Clear image if weather is unsupported or directory missing
                    self.clear_image()
            else:
                # Clear image if error response from API
                self.clear_image()


# Run the file
MyGUI()