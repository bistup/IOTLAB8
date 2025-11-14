import umqtt.robust as umqtt

HOSTNAME = '172.20.10.2'
PORT = 8080
TOPIC = 'temp/pico'

mqtt = umqtt.MQTTClient(
    client_id = b'publish',
    server = HOSTNAME.encode(),
    port = PORT,
    keepalive = 7000
    )

mqtt.connect()

mqtt.publish(TOPIC, str("20").encode())