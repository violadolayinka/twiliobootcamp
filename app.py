from bootcamp import StudentApp
import requests
import json


app = StudentApp("Viola")

cities = {
    "San Francisco":"60 and cloudy",
    "Houston":"80 and muggy",
    "Cleveland":"32 and snowing",
}

@app.route('/weather')
def weather():
    city = request.values.get('city', 'San Francisco')
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&"
    response = requests.get(url)
    json = json.loads(response.content)
    tempK = json.get("main").get("temp")
    return "The weather in {city} is {weather} Kelvin".format(city=city, weather=tempK)

    # weather = cities.get(city, "[WEATHER DATA UNAVAILABLE]")
    # return "The weather in {city} is {weather}".format(city=city, weather=weather)

@app.route('/business_phone')
def business_phone():
    if app.available:
        return """<?xml version="1.0" encoding="UTF-8"?>
        <Response>
          <Dial>+12672502802</Dial>
        </Response>"""
    else:
        return """<?xml version="1.0" encoding="UTF-8"?>
        <Response>
          <Say>Viola is unavailable</Say>
          <Record action = "/hangup" />
        </Response>"""

@app.route('/recordings')
def show_recordings():
    api = "https://api.twilio.com/2010-04-01"
    uri = "/Accounts/" + ACCOUNT_SID + "/Recordings.json"
    credentials = (ACCOUNT_SID,ACCOUNT_TOKEN)
    response = requests.get(api + uri, auth=credentials)
    recordings = json.loads(response.content)
    return app.display_recordings(recordings)

app.run()
