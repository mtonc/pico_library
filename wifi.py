from network import WLAN, STA_IF
import secrets
from led import led
from time import sleep

def connect():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(secrets.WIFI_SSID, secrets.PASSWORD)
    sleep(3)
    return wlan.isconnected()