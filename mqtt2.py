from umqtt.simple import MQTTClient
import machine
import time
import network

import ubinascii
import imu1
from time import sleep_ms
from machine import Pin, SoftI2C
#from sh1106 import SH1106_I2C

# ip         192.168.0.180      192.168.1.73   192.168.0.35
# wifi       IZZI-A29C          INFINITUMb6um  IZZI-6906-5G
# contrasena Gnp93R6Ez46HnyahhT f99a41e4b8     3C04610F6906


# Configurar credenciales de red y detalles del broker
WIFI_SSID = "IZZI-6906"
WIFI_PASSWORD = "3C04610F6906"
MQTT_BROKER = "192.168.0.35"
MQTT_CLIENT_ID = 'esp32'
MQTT_TOPIC_X = "MPU_6050"

# Conectarse a la red WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# Esperar a que la conexión a la red WiFi sea exitosa
while wifi.isconnected() == False:
    pass
print('conexion exitosa')
print(wifi.ifconfig())


def conectar():
    global MQTT_CLIENT_ID ,MQTT_BROKER
     # Inicializar el cliente MQTT
    mqtt = MQTTClient(MQTT_CLIENT_ID,MQTT_BROKER)
    mqtt.connect()
    print('conectado')
    return mqtt


def reconectar():
    print('Fallo de conexion.Reconectando....')
    time.sleep(5)
    machine.reset()

try:
    client = conectar()
    print('hola')
except OSError as e:
    print('no lo lograste')
    reconectar()

    
while True:
    try:
    
        # Leer los valores del acelerómetro
        k_angle_x, k_angle_y = imu1.read_mpu6050()
        angulox = str(k_angle_x)
        print(angulox)
       
        # Enviar los valores obtenidos a través de MQTT
        client.publish(MQTT_TOPIC_X ,angulox)
        
        sleep_ms(10)
    except OSError as e:
        reconectar()
