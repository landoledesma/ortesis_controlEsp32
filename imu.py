# IMU MPU6050 or MPU6500/MPU9200
import machine, ubinascii, time, math
from machine import Pin, SoftI2C
from kalman import KalmanAngle


class IMU():
    


#     # Static Variables: 
# 
#     last_read_time = 0.0   
# 
#     # These are the filtered angles
#     last_x_angle = 0.0          
#     last_y_angle = 0.0
#     last_z_angle = 0.0  
# 
#     # Calibrated measurements to offset some bias or error in the readings.
#     calib_x_accel = 0.0 
#     calib_y_accel = 0.0 
#     calib_z_accel = 0.0 
#     calib_x_gyro  = 0.0 
#     calib_y_gyro  = 0.0 
#     calib_z_gyro  = 0.0 

    PWR_MGMT_1   = const(0x6B)
    SMPLRT_DIV   = const(0x19)
    CONFIG       = const(0x1A)
    GYRO_CONFIG  = const(0x1B)
    INT_ENABLE   = const(0x38)
    # HIGH ACCEL
    ACCEL_XOUT_H = const(0x3B)
    ACCEL_YOUT_H = const(0x3D)
    ACCEL_ZOUT_H = const(0x3F)
    # HIGH GYRO
    GYRO_XOUT_H  = const(0x43)
    GYRO_YOUT_H  = const(0x45)
    GYRO_ZOUT_H  = const(0x47)


    def __init__(self, address=0x68, scl_pin=22, sda_pin=21, _freq=400000):
        self.address = address
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin
        self._freq = _freq
        # Static Variables: 
        self.last_read_time = 0.0   

        # These are the filtered angles
        self.last_x_angle = 0.0          
        self.last_y_angle = 0.0
        self.last_z_angle = 0.0  

        # Calibrated measurements to offset some bias or error in the readings.
        self.calib_x_accel = 0.0 
        self.calib_y_accel = 0.0 
        self.calib_z_accel = 0.0 
        self.calib_x_gyro  = 0.0 
        self.calib_y_gyro  = 0.0 
        self.calib_z_gyro  = 0.0
        self.kalmanX = KalmanAngle()
        self.kalmanY = KalmanAngle()
        
    def InitImu(self):
        self.i2c_imu = SoftI2C(scl=machine.Pin(self.scl_pin), sda=machine.Pin(self.sda_pin), freq=self._freq)
        self.i2c_imu.writeto_mem(self.address, SMPLRT_DIV, b'\x07')
        self.i2c_imu.writeto_mem(self.address, PWR_MGMT_1, b'\x00')
        self.i2c_imu.writeto_mem(self.address, CONFIG, b'\x00')
        self.i2c_imu.writeto_mem(self.address, GYRO_CONFIG, b'\x18')
        self.i2c_imu.writeto_mem(self.address, INT_ENABLE, b'\x00')
    
    def GetRawData(self, reg_addr):
        self.reg_addr = reg_addr
        self.high_read = self.i2c_imu.readfrom_mem(self.address, self.reg_addr, 1)
        self.low_read = self.i2c_imu.readfrom_mem(self.address, self.reg_addr+1, 1)
        self.val = self.high_read[0] << 8 | self.low_read[0]
        
        if (self.val > 32768):
            self.val = self.val - 65536
            
        return self.val


    def ReadImu(self):
        try:
            self.t_now = time.ticks_ms()
            self.dt = (self.t_now - self.GetLastTime())/1000.0
            self.acc_x, self.acc_y, self.acc_z, self.gyro_x, self.gyro_y, self.gyro_z = self.GetValuesHelper()
            
            #Full scale range +/- 250 degree/C as per sensitivity scale factor. The is linear acceleration in each of the 3 directions ins g's
            self.Ax = self.acc_x/16384.0
            self.Ay = self.acc_y/16384.0
            self.Az = self.acc_z/16384.0

            # This is angular velocity in each of the 3 directions 
            self.Gx = (self.gyro_x - self.calib_x_gyro)/131.0
            self.Gy = (self.gyro_y - self.calib_y_gyro)/131.0
            self.Gz = (self.gyro_z - self.calib_z_gyro)/131.0
            self.acc_angles = self.AccAngle(self.Ax, self.Ay, self.Az) # Calculate angle of inclination or tilt for the x and y axes with acquired acceleration vectors
            self.gyr_angles = self.GyrAngle(self.Gx, self.Gy, self.Gz, self.dt) # Calculate angle of inclination or tilt for x,y and z axes with angular rates and dt
            
            (self.c_angle_x, self.c_angle_y) = self.CFilteredAngle(self.acc_angles[0], self.acc_angles[1], self.gyr_angles[0], self.gyr_angles[1]) # filtered tilt angle i.e. what we're after
            (self.k_angle_x, self.k_angle_y) = self.KFilteredAngle(self.acc_angles[0], self.acc_angles[1], self.Gx, self.Gy, self.dt)
            self.SetLastReadAngles(self.t_now, self.c_angle_x, self.c_angle_y)
            
            return (self.k_angle_x, self.k_angle_y)
        
        except:
            pass


    def CalibrateSensor(self):
        self.x_accel = 0
        self.y_accel = 0
        self.z_accel = 0
        self.x_gyro  = 0
        self.y_gyro  = 0
        self.z_gyro  = 0

        self.GetValuesHelper()
        
        for int in range(10):
            self.values = self.GetValuesHelper()
            self.x_accel += self.values[0]
            self.y_accel += self.values[1]
            self.z_accel += self.values[2]
            self.x_gyro  += self.values[3]
            self.y_gyro  += self.values[4]
            self.z_gyro  += self.values[5]
            time.sleep_ms(100)
           

        self.x_accel /= 10
        self.y_accel /= 10
        self.z_accel /= 10
        self.x_gyro  /= 10
        self.y_gyro  /= 10
        self.z_gyro  /= 10

        self.calib_x_accel = self.x_accel
        self.calib_y_accel = self.y_accel
        self.calib_z_accel = self.z_accel
        self.calib_x_gyro  = self.x_gyro
        self.calib_y_gyro  = self.y_gyro
        self.calib_z_gyro  = self.z_gyro


    def SetLastReadAngles(self, time, x, y):
        self.last_read_time = time
        self.last_x_angle = x
        self.last_y_angle = y
        #last_z_angle = z


    def AccAngle(self, Ax, Ay, Az):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.rad_2_deg = 180/3.141592
        self.ax_angle  = math.atan(self.Ay/math.sqrt(math.pow(self.Ax,2) + math.pow(self.Az, 2)))*self.rad_2_deg
        self.ay_angle = math.atan((-1*self.Ax)/math.sqrt(math.pow(self.Ay,2) + math.pow(self.Az, 2)))*self.rad_2_deg
        return (self.ax_angle, self.ay_angle)


    def GyrAngle(self, gx, gy, gz, dt):
        self.gx = gx
        self.gy = gy
        self.gz = gz
        self.dt = dt
        self.gx_angle = self.gx*self.dt + self.GetLastXAngle()
        self.gy_angle = self.gy*self.dt + self.GetLastYAngle()
        self.gz_angle = self.gz*self.dt + self.GetLastZAngle()
        return (self.gx_angle, self.gy_angle, self.gz_angle)


    def CFilteredAngle(self, ax_angle, ay_angle, gx_angle, gy_angle):
        self.ax_angle = ax_angle
        self.ay_angle = ay_angle
        self.gx_angle = gx_angle
        self.gy_angle = gy_angle
        self.alpha = 0.90
        self.c_angle_x = self.alpha*self.gx_angle + (1.0-self.alpha)*self.ax_angle
        self.c_angle_y = self.alpha*self.gy_angle + (1.0-self.alpha)*self.ay_angle
        return (self.c_angle_x, self.c_angle_y)



    def KFilteredAngle(self, ax_angle, ay_angle, Gx, Gy, dt):
        self.ax_angle = ax_angle
        self.ay_angle = ay_angle
        self.Gx = Gx
        self.Gy = Gy
        self.dt = dt
        self.k_angle_x = self.kalmanX.getAngle(self.ax_angle, self.Gx, self.dt)
        self.k_angle_y = self.kalmanY.getAngle(self.ay_angle, self.Gy, self.dt)
        return (self.k_angle_x, self.k_angle_y)


    def GetValuesHelper(self):
        self.acc_x = self.GetRawData(ACCEL_XOUT_H)
        self.acc_y = self.GetRawData(ACCEL_YOUT_H)
        self.acc_z = self.GetRawData(ACCEL_ZOUT_H)
        self.gyro_x = self.GetRawData(GYRO_XOUT_H)
        self.gyro_y = self.GetRawData(GYRO_YOUT_H)
        self.gyro_z = self.GetRawData(GYRO_ZOUT_H)

        return (self.acc_x, self.acc_y, self.acc_z, self.gyro_x, self.gyro_y, self.gyro_z)


    def GetLastTime(self): 
        return self.last_read_time
    

    def GetLastXAngle(self):
        return self.last_x_angle


    def GetLastYAngle(self):
        return self.last_y_angle


    def GetLastZAngle(self):
        return self.last_z_angle

