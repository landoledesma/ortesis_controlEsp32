# Read Imu
import time
import imu
from time import sleep_ms, sleep
from machine import Pin, SoftI2C, ADC, PWM
# Motor control
from dcmotor import DCMotor       
from machine import Pin, PWM   


# Motor pins: (L298N)
frequency = 15000
pin1 = Pin(4, Pin.OUT)     
pin2 = Pin(5, Pin.OUT)     
enable = PWM(Pin(2), frequency) # Enable pin
dc_motor = DCMotor(pin1, pin2, enable, min_duty=350, max_duty=1023)


while True:
    dc_motor.backward(100)
    sleep(3)
    dc_motor.stop()
    sleep_ms(500)
    dc_motor.forward(100)
    sleep(5)
    dc_motor.stop()
    sleep_ms(500)
    dc_motor.backward(100)
    sleep(5)
    dc_motor.stop()
    sleep_ms(500)
    dc_motor.forward(100)
    sleep(10)
    dc_motor.stop()
    sleep_ms(500)
            