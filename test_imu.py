import imu
from time import sleep_ms, sleep
from machine import Pin, SoftI2C

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

while True:
    
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
        print(knee)
        
        sleep_ms(20)



