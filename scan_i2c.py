from machine import Pin, SoftI2C

i2c = SoftI2C(scl=Pin(22),sda=Pin(21),freq=400000)

print(i2c.scan())