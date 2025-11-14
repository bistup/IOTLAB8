import umqtt.robust as umqtt
from network import WLAN
import time
import socket
from machine import Pin, PWM, ADC, Timer

#set up wifi
wifi = WLAN(WLAN.IF_STA)
wifi.active(True)

ssid =  'LimaPhone'
password = '12345678'

#set hostname and ports and topic to send
HOSTNAME = '172.20.10.2'
PORT = 8080
TOPIC = b"temp/pico"

#set up mqtt client
mqtt = umqtt.MQTTClient(
    client_id = b'publish',
    server = HOSTNAME.encode(),
    port = PORT,
    keepalive = 7000
    )

mqtt.connect()

#set temp
temp_sensor = ADC(4)

#Read the temp
def read_temp():
    global temp_sensor
    value = temp_sensor.read_u16()
    voltage = value * (3.3 / 2 ** 16)
    temperature = 27 - (voltage - 0.706) / 0.001721
    return temperature

#send the temp
def send_temperature():
    client_socket = None
    try:
        temperature = read_temp()
        print(f"Temperature: {temperature:.2f} degrees celcius") 
        mqtt.publish(TOPIC, str(temperature).encode())
    except Exception as e:
        print(f"Error in send_temperature: {e} ")


def timer_callback(t):
    send_temperature()


timer = Timer()

#initialize timer
timer.init(freq = 0.5, mode=Timer.PERIODIC, callback = timer_callback)
