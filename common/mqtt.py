from umqtt.simple import MQTTClient
import secrets
import time
import machine

client_id = 'mtonc_pico_1'
temp = b'env/temperature'
pres = b'env/pressure'
humid = b'env/humidity'

def connect(attempts = 3):
    if attempts > 0:
        try:
            client = MQTTClient(client_id, secrets.MQTTIP, user=secrets.MQTTUSER, password=secrets.MQTTPASS, keepalive=3600)
            client.connect()
            time.sleep(3)
            print('Connected to %s MQTT Broker'%(secrets.MQTTIP))
            return client
        except OSError as e:
            print(e)
            return connect(attempts - 1)
    else:
        print('Unable to connect to mqtt broker')