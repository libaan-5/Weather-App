import requests
import json

API_KEY = "API_KEY"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city, country_code=None, units=None): 
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
        print(f"Country: {country}, Weather in {name}: {weather}, Temperature: {temp}{unit_symbol}\n")
        
        # print(json.dumps(data, indent=4))

    # Error messages below    
    elif response.status_code == 400:
        print("Error 400: Bad request (maybe missing parameters or invalid query).")
    elif response.status_code == 401:
        print("Error 401: Invalid API key.")
    elif response.status_code == 404:
        print("Error 404: City not found (incorrect input).")
    elif response.status_code == 429:
        print("Error 429: Too many requests – you’ve hit the API limit.")
    else:
        print(f"Error {response.status_code}: Unexpected API error.")

def main():
    while True:
        user_input = input("Enter city name (optionally with country code, e.g., 'London,US') or 'quit' to exit: ").strip() # Eliminates white-space (before or after input)

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
            break
        get_weather(city, country_code, units)


if __name__ == "__main__":
    main()
