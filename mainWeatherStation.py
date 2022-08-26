from machine import Pin, I2C
from DHT22 import DHT22
import time
import rp2
from bmp085 import BMP180
import network
from umqtt.simple import MQTTClient

dht22 = DHT22(Pin(2,Pin.IN,Pin.PULL_UP))
i2c = I2C(0, scl=Pin(21), sda=Pin(20))
bmp = BMP180(i2c)

rp2.country('GB')
ssid = ''
password = ''

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

mqtt_server = 'broker.hivemq.com'
client_id = 'muzweather'
topic_pub = b'muztemp'

def tempRead():
    # take temperature from DHT22
    temperature_C, humidity = dht22.read()
    rp2.PIO(0).remove_program()
    return temperature_C

def humidityRead():
    # take humidity from DHT22
    temperature_C, humidity = dht22.read()
    rp2.PIO(0).remove_program()
    return humidity
    
def pressureRead():
    # take air pressure from BMP180
    bmp = BMP180(i2c)
    pressure = bmp.pressure
    return pressure
    
def altitudeRead():
    # take altitude from BMP180
    bmp = BMP180(i2c)
    altitude = bmp.altitude
    return altitude

def lightRead():
    sensor = machine.ADC(28)
    light = int(sensor.read_u16())
    return light

def wifiConnect():
    return 0

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   time.sleep(5)
   machine.reset()

def main():
    
    
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    try:
        client = mqtt_connect()
    except OSError as e:
       reconnect()
       
    print(tempRead())
    print(humidityRead())
    print(pressureRead())
    print(altitudeRead())
    print(lightRead())
    publishString = str(tempRead()) + "," + str(humidityRead()) + "," + str(pressureRead()) + "," + str(altitudeRead()) + "," + str(lightRead())
    client.publish(topic_pub, publishString)
    time.sleep(600)

while(True):
    main()


    

    
