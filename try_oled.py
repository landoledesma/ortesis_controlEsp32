#More details can be found in TechToTinker.blogspot.com 
# George Bantique | tech.to.tinker@gmail.com

from machine import Pin 
from machine import I2C 
from machine import RTC 
from time import sleep_ms 
from machine import Pin, I2C
from sh1106 import SH1106_I2C

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
oled = SH1106_I2C(128, 64, i2c, None, addr=0x3C)
oled.sleep(False)

rtc = RTC() 
rtc.datetime((2021, 2, 6, 6, 19, 44, 0, 0)) 
# rtc.datetime((YYYY, MM, DD, WD, HH, MM, SS, MS)) 
# WD 1 = Monday 
# WD 7 = Sunday 
isPoint = True

while True: 
    t = rtc.datetime() 
    oled.fill(0) 
    oled.text('** 1.3 OLED **', 4, 0) 
    oled.text('Date: {}-{:02d}-{:02d}' .format(t[0],t[1],t[2]), 0, 25)  
    if isPoint: 
        colon = ':' 
    else: 
        colon = ' ' 
    oled.text('Time: {:02d}{}{:02d}' .format(t[4], colon, t[5]), 0, 40) 
    oled.show() 
    sleep_ms(500) 
    isPoint = not isPoint