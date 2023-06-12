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

input("Press enter to start measuring")
i = 0
angle = []

while i<= 180:
    
        angle_femx, angle_femy = af1.ReadImu()
        #angle_femx = round(k_angle_x_fem,2)
        sleep_ms(5)
        
        angle_tibx, angle_tiby = at2.ReadImu()
        #angle_tibx = round(k_angle_x_tib,2)
        #angle_tiby = round(k_angle_y_tib,2)
        sleep_ms(5)
        '''        
        if angle_femx < 0 and angle_tibx < 0:
            knee = 180 + angle_femx + angle_tibx
        elif angle_femx < 0 and angle_tibx > 0:
            knee = 180 + angle_femx - angle_tibx
        elif angle_femx > 0 and angle_tibx < 0:
            knee = 180 + angle_femx + angle_tibx
        else:
        '''
        '''
        dev_fem = 90 + (angle_femx)
        dev_tib = 90 + (angle_tibx)
        knee = 180 + (dev_fem) + (dev_tib)
        '''
        theta = 180 + angle_femy - angle_tiby
        knee = 180 - theta
        print(knee)
        
        angle.append(knee)
         
        
        #print(angle_femx,angle_femy, angle_tibx, angle_tiby)
        #sleep_ms(30)
        i += 1

angles = [str(value) for value in angle]

# Unimos todas las cadenas con una nueva línea
text = "\n".join(angles)

# Guardamos el texto en un archivo
file = open("angles.txt", "w")
file.write(text)
file.close()


