from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)

def on():
    led.on()
    
def off():
    led.off()