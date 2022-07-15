import argparse
import sys  # exit the program without a traceback
import json
from configparser import ConfigParser
from urllib import error, parse, request
import style


BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Weather Condition Code
THUNDERSTORM = range(200, 300)


# get access to API key
# function should be considered non-public:
def _get_api_key():
    """it’ll return the value of your OpenWeather API key, which is ready to use in your API requests"""
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]


# command-line input parser that takes user-provided information for a city
# and an optional parameter about what temperature scale to use
def read_user_cli_args():
    """Handles the CLI user interactions"""
    parser = argparse.ArgumentParser(description="gets weather and temperature information for a city")

    parser.add_argument(
        "city", nargs="+", type=str, help="enter the city name"
    )   # nargs="+" allow users to pass city names that are made up of more than one word
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial units",
    )   # the value for imperial will be True if users add the optional flag, and False if they don’t
    return parser.parse_args()


# Build the URL
def build_weather_query(city_input):
    """Builds the URL for an API request to OpenWeather's weather API"""
    # city_input is the list of strings collected in user_args.city
    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)  # encodes the string to make a valid HTTP request to the API
    url = (f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
           f"&appid={api_key}")
    return url


# convert the data of the API response into a Python dictionary
def get_weather_data(query_url):
    """Makes an API request to a URL and returns the data as a Python object"""
    # make an HTTP GET request to the query_url parameter and saves the result as response
    response = request.urlopen(query_url)

    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401:  # 401 - Unauthorized
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404:  # 404 - Not Found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong... ({http_error.code})")

    data = response.read()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't read the server response.")


def display_weather_info(weather_data):
    """Prints formatted weather information about a city"""

    city = weather_data["name"]
    weather_id = weather_data["weather"][0]["id"]

    style.change_color(style.REVERSE)
    print(f"{city:^{style.PADDING}}", end="")
    style.change_color(style.RESET)

    weather_symbol, color = _select_weather_display_params(weather_id)

    style.change_color(color)

    style.change_color(style.RESET)
    print(f"\t{weather_symbol}", end=" ")
    print(f"({'No storm today! :p' if weather_id not in THUNDERSTORM else 'Brace yourself today! :c'})")


def _select_weather_display_params(weather_id):
    if weather_id in THUNDERSTORM:
        display_params = ("🌩️", style.RED)
    elif weather_id not in THUNDERSTORM:
        display_params = ("✨", style.YELLOW)
    else:  # In case the API adds new weather codes
        display_params = ("🌈", style.RESET)
    return display_params


if __name__ == "__main__":
    print('THUNDERSTORM CHECKER')
    user_args = read_user_cli_args()
    query_url = build_weather_query(user_args.city)
    weather_data = get_weather_data(query_url)
    display_weather_info(weather_data)
