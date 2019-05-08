# Microcontroller input pin
PIN_FLOATER = 4

# WiFi ID and passowrd to connect the Microcontroller
WIFI_SSID = "xxxxx"
WIFI_PWD = "xxxx"

# Telerivet API credentials to send a message, POST /v1/projects/<project_id>/messages/send
# See https://telerivet.com/api/rest#Project.sendMessage for more
API_KEY = "<TELERIVET_API_KEY>"
PROJECT_ID = "<TELERIVET_PROJECT_ID>"
BASE_URL = "https://api.telerivet.com/v1/projects/{}".format(PROJECT_ID)
SMS_POST_URL = "{}/messages/send".format(BASE_URL)
# Phone number to send the message to
RECIPIENT_NUMBER = "+xxxxxxx"

TANK_ID = "Tank 1"
# Content of the message to send
MESSAGE_TEXT = "Warning!! Water level low in {}".format(TANK_ID)