# Read Imu
import math
import imu
from time import sleep_ms, sleep
from machine import Pin, SoftI2C,PWM
from sh1106 import SH1106_I2C

# Motor control
from dcmotor import DCMotor
from Routines import routine_total

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000) 
oled = SH1106_I2C(128, 64, i2c, None, addr=0x3C)
oled.sleep(False)

#oled
oled.fill(0) 
oled.text('**REX**', 40, 0)
oled.text('UPIITA', 40 ,10)
oled.show()

#leer IMU1
af1 = imu.IMU(address=0x69)
af1.InitImu()
af1.CalibrateSensor()

oled.text('A1 Init',0, 35)
oled.show()
#print("Femur accelerometer succesfully initializated")

#Leer IMU2
#Tibia accelerometer
at2 = imu.IMU()
at2.InitImu()
at2.CalibrateSensor()
#print("Tibia accelerometer succesfully initializated")
oled.text("A2 Init", 0, 45)
oled.show()

# Motor pins: (L298N)
frequency = 15000
pin1 = Pin(4, Pin.OUT)     
pin2 = Pin(5, Pin.OUT)     
enable = PWM(Pin(2), frequency) # Enable pin
dc_motor = DCMotor(pin1, pin2, enable, min_duty=350, max_duty=1023)

#Femur accelerometer:

i = 0
while True:
    
    for i, valor in enumerate(routine_total):
    
        angle_femx, angle_femy = af1.ReadImu()
        #angle_femx = round(k_angle_x_fem,2)
        sleep_ms(100)
            
        angle_tibx, angle_tiby = at2.ReadImu()
        #angle_tibx = round(k_angle_x_tib,2)
        #angle_tiby = round(k_angle_y_tib,2)
        sleep_ms(100)
           
        theta = 180 + angle_femy - angle_tiby
        #print(angle_femy,angle_tiby)
        
        
        knee = 180 - theta
        knee = math.ceil(knee)
        desired_value = math.ceil(abs(valor))
    
        
        while desired_value != knee:
            oled.fill(0)
            oled.text("Reading...", 25, 0)
            oled.show()
            oled.text(f'AC: {knee}', 40, 25)
            oled.show()
            oled.text(f'DA: {desired_value}',40, 40)
            oled.show()
            #print(knee,desired_value)
            angle_femx, angle_femy = af1.ReadImu()
            #angle_femx = round(k_angle_x_fem,2)
            sleep_ms(100)
                
            angle_tibx, angle_tiby = at2.ReadImu()
            #angle_tibx = round(k_angle_x_tib,2)
            #angle_tiby = round(k_angle_y_tib,2)
            sleep_ms(100)
               
            theta = 180 + angle_femy - angle_tiby
            #print(angle_femy,angle_tiby)
                
            knee = 180 - theta
            knee = math.ceil(knee)
            sleep_ms(500)
            if desired_value > knee:
                dc_motor.backward(100)    
            elif desired_value < knee:
                dc_motor.forward(100)
            


        
        
        
            
        sleep_ms(20)
