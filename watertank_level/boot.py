from machine import RTC, deepsleep
import utime
import urequests

import settings # Load our configuration file
# http://docs.micropython.org/en/v1.9.3/esp8266/esp8266/tutorial/network_basics.html
def do_connect():
    import network
    import utime
    print("Connecting to WiFi...")
    sta_if = network.WLAN(network.STA_IF); 
    sta_if.active(True)
    sta_if.connect(settings.WIFI_SSID, settings.WIFI_PWD)

    tmo = 50
    while not sta_if.isconnected():
        utime.sleep_ms(100)
        tmo -= 1
        if tmo == 0:
            print("Failed to connect WiFi")
            return False
    if tmo > 0:
        ifcfg = sta_if.ifconfig()
        print("WiFi started, IP:", ifcfg[0])
        utime.sleep_ms(500)
        return True

def do_sms_post_request(): 
    import ujson
    headers = {'Content-Type': 'application/json'}
    data = {"api_key": settings.API_KEY, "content": settings.MESSAGE_TEXT, "to_number": settings.RECIPIENT_NUMBER}
    return urequests.post(settings.SMS_POST_URL, data = ujson.dumps(data), headers = headers)

def do_deep_sleep(floater):
    print("Water level is OK. Going to sleep..")
    # Ref https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/rtc
    rtc = RTC()
    rtc.ntp_sync(server="hr.pool.ntp.org", tz="CET-1CEST")
    rtc.synced()
    rtc.wake_on_ext0(floater, 0)

    # ESP32 power reduction for battery powered 
    # https://forum.micropython.org/viewtopic.php?t=3900
    deepsleep(0)
