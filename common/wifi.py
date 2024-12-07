from network import WLAN, STA_IF
import secrets
from time import sleep
import led

def connect(retry = 3):
    wlan = WLAN(STA_IF)
    wlan.config(pm=wlan.PM_PERFORMANCE)
    wlan.active(True)
    if retry > 0:
        wlan.connect(secrets.WIFI_SSID, secrets.PASSWORD)
        sleep(3)
        if wlan.isconnected():
            led.on()
            return True
        else:
            return connect(retry - 1)
    else:
        wlan.connect(secrets.BACKUP_WIFI, secrets.BACKUP_PASSWORD)
        sleep(3)
        return wlan.isconnected()