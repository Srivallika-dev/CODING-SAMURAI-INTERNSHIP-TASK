
import requests

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    """Fetch and display weather data for a given city."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            print(f"Error: {data.get('message', 'Unable to fetch weather data.')}")
            return

        city_name = data["name"]
        country = data["sys"]["country"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        print("\n===== Weather Report =====")
        print(f"Location     : {city_name}, {country}")
        print(f"Temperature  : {temperature}°C")
        print(f"Feels Like   : {feels_like}°C")
        print(f"Humidity     : {humidity}%")
        print(f"Condition    : {description.capitalize()}")

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")


def main():
    """Main program loop."""
    print("===== Weather Application =====")

    while True:
        city = input("\nEnter city name (or type 'exit' to quit): ").strip()

        if city.lower() == "exit":
            print("Exiting Weather App. Goodbye!")
            break

        if city:
            get_weather(city)
        else:
            print("City name cannot be empty.")


if __name__ == "__main__":
    main()
