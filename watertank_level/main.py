from machine import Pin
import utime

import settings # Load our configuration file

# Initialise the water lever floater sensor. 
# Make sure to connect the pins to GND(Power) and number given in settings.PIN_FLOATER
floater = Pin(settings.PIN_FLOATER, Pin.IN, Pin.PULL_UP)

# TODO: Add comments..
if floater.value() == 0:
    print("Water level warning!")
    if do_connect():
        utime.sleep(2)
        print("Sending SMS")
        try:
            response = do_sms_post_request()
        except:
            # Posting the request sometimes fails on the first atampt.
            # Retrying on the second time does works.
            # TODO: Handle error and improve retry 
            print("try again")
            response = do_sms_post_request()
        print(response.json())
    else:
        print("Failed to connect to WiFi")
else:
    do_deep_sleep(floater)

