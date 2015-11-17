from bootcamp import StudentApp

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
          <Say>Alice is unavailable</Say>
          <Record action = "/hangup" />
        </Response>"""

app.run()
