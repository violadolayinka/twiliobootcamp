from bootcamp import StudentApp
import requests
import json

ACCOUNT_SID = "AC08104111c524d56d95117df1d60f2283"
ACCOUNT_TOKEN = "d5429aa8bd9592b9fd94c0a3b8a9877c"

app = StudentApp("Viola")

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

app.run()
