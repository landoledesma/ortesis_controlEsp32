# Read Imu
import imu
from time import sleep_ms, sleep, ticks_ms
from machine import Pin, SoftI2C, ADC, PWM
# Motor control
from dcmotor import DCMotor       
from machine import Pin, PWM   
# PID control
from PID import PID
# Routines:
from Routines import routine_total

print(type(routine_total))

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
pid = PID(kp=2.00, ki=0, kd=2.0, _type='PD')
t = ticks_ms()


while True:
    
        i = 0
        t0 = 0
        
        for i, valor in enumerate(routine_total):
            
            angle_femx, angle_femy = af1.ReadImu() 
            sleep_ms(20)
            print(1)
        
            angle_tibx, angle_tiby = at2.ReadImu()
            sleep_ms(20)
            
            theta = 180 + angle_femy - angle_tiby   
            current_position = 180 - theta
            
            desired_position = 30
            
            error = desired_position - current_position
            
            t1 = ticks_ms()
            
            dt = (t1 - t0)/1e3
            
            output = pid.update(error, dt)
            #duty = pid.duty_cycle(abs(output))
            #pwm.duty(duty)
            if output <= 0:
                dc_motor.backwards(100)
            elif output >= 0:
                dc_motor.forward(100)
            
            sleep_ms(100)