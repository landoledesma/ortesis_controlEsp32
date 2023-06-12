
# Read Imu
import imu
from time import sleep_ms, sleep
from machine import Pin, SoftI2C,PWM

# Motor control
from dcmotor import DCMotor       
#from machine import Pin, PWM



af1 = imu.IMU(address=0x69)
af1.InitImu()
af1.CalibrateSensor()
print("Femur accelerometer succesfully initializated")

#Tibia accelerometer
at2 = imu.IMU()
at2.InitImu()
at2.CalibrateSensor()
print("Tibia accelerometer succesfully initializated")


# Motor pins: (L298N)
frequency = 15000
pin1 = Pin(4, Pin.OUT)     
pin2 = Pin(5, Pin.OUT)     
enable = PWM(Pin(2), frequency) # Enable pin
dc_motor = DCMotor(pin1, pin2, enable, min_duty=350, max_duty=1023)


#Femur accelerometer:


while True:
    
    desired_value = 30
    
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
    print("HOLA RODILLA:", knee)
    
    
    
    if desired_value > knee:
        dc_motor.backward(100)    
    elif desired_value < knee:
        dc_motor.forward(100)
    
    print("ADIOS RODILLA: ", knee)
    
        
    sleep_ms(20)



