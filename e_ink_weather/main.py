from urllib import urequest
from machine import Pin, RTC
from picographics import PicoGraphics, DISPLAY_INKY_PACK
from wifi import connect
import ujson
from secrets import WX_API_KEY, LOCATION
import led
from sys import exit

# Buttons
button_a = Pin(12, Pin.IN, pull=Pin.PULL_UP)
button_b = Pin(13, Pin.IN, pull=Pin.PULL_UP)
button_c = Pin(14, Pin.IN, pull=Pin.PULL_UP)

# Display
graphics = PicoGraphics(DISPLAY_INKY_PACK)
graphics.clear()
WIDTH, HEIGHT = graphics.get_bounds()
graphics.set_update_speed(3)
graphics.set_font("sans")

base_url = 'http://api.weatherapi.com/v1/'

graphics.set_pen(15)
graphics.clear()
graphics.set_pen(0)
graphics.set_thickness(2)

weather = None
forecast = None

def get_weather(*args):
    global weather
    if weather == None:
        query = '?key=' + WX_API_KEY + '&q=' + LOCATION + '&aqi=yes'
        url = base_url + 'current.json' + query
        try:
            res = urequest.urlopen(url)
        except Exception as e:
            print(e)
        else:
            weather = ujson.loads(res.readline())
    draw_weather(**weather)

def calc_offset(text, scale):
    return int((WIDTH/2) - (graphics.measure_text(text, scale)/2))

def draw_weather(location, current):
    graphics.set_pen(15)
    graphics.clear()
    graphics.clear()
    graphics.set_pen(0)
    graphics.set_thickness(2)
    
    #Forecast text
    cnd_txt = 'Forecast: ' + current['condition']['text']
    cnd_offset = calc_offset(cnd_txt, 0.8)
    graphics.text(cnd_txt, cnd_offset, 20, scale=0.8)
    
    #Temperature
    temp_txt = 'Temp: ' + str(current['temp_f']) + '°F/' + str(current['temp_c']) + '°C'
    temp_offset = calc_offset(temp_txt, 0.66)
    graphics.text(temp_txt, temp_offset, 40, scale=0.66)
    
    #Humidity
    hum_txt = 'Humidity: ' + str(current['humidity']) + '%'
    hum_offset = calc_offset(hum_txt, 0.66)
    graphics.text(hum_txt, hum_offset, 60, scale=0.66)
    
    #Presssure
    press_txt = 'Pressure: ' + str(current['pressure_mb']) + 'mb'
    press_offset = calc_offset(press_txt, 0.66)
    graphics.text(press_txt, press_offset, 80, scale=0.66)
    
    #Air Quality Index
    aqi_txt = 'US EPA AQI: ' + str(current['air_quality']['us-epa-index'])
    aqi_offset = calc_offset(aqi_txt, 0.66)
    graphics.text(aqi_txt, aqi_offset, 100, scale=0.66)
    
    graphics.update()
    
def get_forecast(*args):
    global forecast
    if not forecast:
        query = '?key=' + WX_API_KEY + '&q=' + LOCATION + '&aqi=no&days=3'
        url = base_url + 'forecast.json' + query
        try:
            res = urequest.urlopen(url)
        except Exception as e:
            print(e)
        else:
            forecast = ujson.loads(res.readline())
    draw_forecast(**forecast)
    
def draw_forecast(location, current, forecast):
    graphics.set_pen(15)
    graphics.clear()
    graphics.clear()
    graphics.set_pen(0)
    graphics.set_thickness(2)
    
    i = 0
    col_wth = (WIDTH//3)
    
    for day in forecast['forecastday']:
        cnd_txt = day['day']['condition']['text']
        lo = 'Lo:' + str(day['day']['mintemp_f']) + '°F'
        high = 'High:' + str(day['day']['maxtemp_f']) + '°F'
        rain = int(day['day']['daily_chance_of_rain'])
        snow = int(day['day']['daily_chance_of_snow'])
        precip = ''
        if rain != 0 or snow != 0:
            precip += 'Precip: ' + str(rain or snow) + '%'
        offset = 5 + (i * col_wth)
        
        graphics.text(cnd_txt, offset, 20, scale=0.5)
        graphics.text(lo, offset, 40, scale=0.5)
        graphics.text(high, offset, 60, scale=0.5)
        graphics.text(precip, offset, 80, scale=0.5)
        i += 1
        graphics.line((col_wth * i),0,(col_wth * i) + 2,HEIGHT)
        
    graphics.update()

button_a.irq(trigger=machine.Pin.IRQ_FALLING, handler=get_weather)
button_b.irq(trigger=machine.Pin.IRQ_FALLING, handler=get_forecast)
#button_c.irq(trigger=machine.Pin.IRQ_FALLING, handler=button)

is_connected = connect()
if is_connected:
    get_weather()
else:
    print('not connected')

led.off()
exit()