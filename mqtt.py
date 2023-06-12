from umqtt.simple import MQTTClient
import machine
import time
import network
import ubinascii
import imu
from time import sleep_ms

class ESP32MQTT:
    def __init__(self, wifi_ssid, wifi_password, mqtt_broker, mqtt_client_id):
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.mqtt_broker = mqtt_broker
        self.mqtt_client_id = mqtt_client_id
        #self.mqtt_topic_x = mqtt_topic_x
        self.wifi = network.WLAN(network.STA_IF)

    def connect_wifi(self):
        self.wifi.active(True)
        self.wifi.connect(self.wifi_ssid, self.wifi_password)
        while self.wifi.isconnected() == False:
            pass
        print('Conexión exitosa')
        print(self.wifi.ifconfig())

    def connect_mqtt(self):
        self.mqtt = MQTTClient(self.mqtt_client_id, self.mqtt_broker)
        self.mqtt.connect()
        print('Conectado a MQTT')

    def publish_data(self,angle,topic):
        try:
            angle = str(angle)
            self.mqtt.publish(topic, angle)
            sleep_ms(100)
        except OSError as e:
            self.reconnect()

    def reconnect(self):
        print('Fallo de conexión. Reconectando...')
        time.sleep(5)
        machine.reset()