import tkinter as tk
from tkinter import ttk

import requests
import json
from dotenv import load_dotenv
import os

# Read environment variables from .env (used for storing API credentials securely)
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

class MyGUI:
    def __init__(self):
        # --------------------------
        # Tkinter window setup
        # --------------------------
        self.root = tk.Tk()   # store in self
        self.root.title("Weather App")

        # Customize the window size here (width x height)
        self.root.geometry("300x200")  # Example: 500px wide, 400px tall

        # Input field
        self.entry = ttk.Entry(self.root, width=40)  # store in self
        self.entry.pack(pady=30)

        # Button to submit input
        button = ttk.Button(self.root, text="Submit", command=self.submit)
        button.pack()

        # Output label (empty at start)
        self.output_label = tk.Label(self.root, text="", font=('Arial', 12))
        self.output_label.pack(pady=10)

        self.root.mainloop()  # start event loop here

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
            name = data["name"]
            country = data["sys"]["country"]
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            unit_symbol = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
            output_weather = f"Country: {country},\n Weather in {name}: {weather},\n Temperature: {temp}{unit_symbol}\n"
            
            return output_weather
            
            # print(json.dumps(data, indent=4))

        # Handle error responses
        error_messages = {
            400: "Error 400: Bad request (maybe missing parameters or invalid query).",
            401: "Error 401: Invalid API key.",
            404: "Error 404: City not found (incorrect input).",
            429: "Error 429: Too many requests – you’ve hit the API limit."
        }

        return error_messages.get(
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

# Run the app
MyGUI()