import requests

API_KEY = "WEATHER_API_KEY"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    }
    response = requests.get(BASE_URL, params=params)
    
    # If the input was valid and everything went well
    if response.status_code == 200:
        data = response.json()
        name = data["name"]
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        print(f"Weather in {name}: {weather}, Temperature: {temp}°C")
        
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
        city = input("Enter city name (or 'quit' to exit): ").strip() # Eliminates white-space (before or after input)
        if city.lower() in ["quit", "exit"]:
            print("Goodbye! 👋")
            break
        get_weather(city)

if __name__ == "__main__":
    main()
