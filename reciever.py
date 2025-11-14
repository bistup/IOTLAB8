import umqtt.robust as umqtt
from network import WLAN
import time, socket
from machine import Timer

wifi = WLAN(WLAN.IF_STA)
wifi.active(True)

ssid = "LimaPhone"
password = "12345678"
wifi.connect(ssid, password)

HOSTNAME = "172.20.10.2"
PORT = 8080
TOPIC = 'temp/pico'

mqtt = umqtt.MQTTClient(
        client_id = b'subscribe',
        server = HOSTNAME.encode(),
        port = PORT,
        keepalive = 7000
)

led = machine.Pin('LED', machine.Pin.OUT)

def callback(topic, message):
    print(f'I received the message "{message}" for topic "{topic}"')
    try:
        temp = float(message)
        if temp > 25:
            led.value(1)
        else:
            led.value(0)

    except ValueError:
        pass
   
mqtt.connect()
def timer_callback(t):
    mqtt.set_callback(callback)
    mqtt.subscribe(TOPIC)
    mqtt.wait_msg()

timer = Timer()
timer.init(freq = 0.5, mode=Timer.PERIODIC, callback = timer_callback)