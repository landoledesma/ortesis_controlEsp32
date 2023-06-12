# Read Imu
import time
import imu
from time import sleep_ms, sleep
from machine import Pin, SoftI2C, ADC, PWM
# Motor control
from dcmotor import DCMotor       
from machine import Pin, PWM   
# PID control
from PID import PID
# Routines:
from Routines import routine_total

# Motor pins: (L298N)
frequency = 15000
pin1 = Pin(4, Pin.OUT)     
pin2 = Pin(5, Pin.OUT)     
enable = PWM(Pin(2), frequency) # Enable pin
dc_motor = DCMotor(pin1, pin2, enable, min_duty=350, max_duty=1023)

#Femur accelerometer:
af1 = imu.IMU(address=0x69)
af1.InitImu()
af1.CalibrateSensor()
print("Femur accelerometer succesfully initializated")

#Tibia accelerometer
at2 = imu.IMU()
at2.InitImu()
at2.CalibrateSensor()
print("Tibia accelerometer succesfully initializated")

# Initialize PID or PD or PI or P 
pid = PID(kp=2.00, ki=0, kd=2.0)
t0 = 0
#t = time.ticks_ms()

def read_sensor():
    angle_femx, angle_tibx = af1.ReadImu()
    sleep_ms(1)
    angle_femy, angle_tiby = at2.ReadImu()
    theta = 180 + angle_femy - angle_tiby   
    return 180 - theta
    

dc_motor.backward(100)
sleep(2)
dc_motor.stop()
            
     