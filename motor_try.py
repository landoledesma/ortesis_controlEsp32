from dcmotor import DCMotor       
from machine import Pin, PWM   
from time import sleep     
frequency = 15000       
pin1 = Pin(4, Pin.OUT)    
pin2 = Pin(5, Pin.OUT)     
enable = PWM(Pin(2), frequency)
dc_motor = DCMotor(pin1, pin2, enable, 350, 1023)

#max_angle = 50
dc_motor.forward(100)

#dc_motor.backward(100)  
sleep(5)       
