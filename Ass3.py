#Antoine and Mariam

from machine import Pin, ADC, I2C
import i2c_lcd
import time
from hcsr04 import HCSR04
 
 #setup
i2c_device = I2C(0, scl=Pin(22), sda=Pin(21))
lcd = i2c_lcd.I2cLcd(i2c_device, 0x27, 2, 16)
sensor = HCSR04(trigger_pin=33, echo_pin=32)
led_1 = Pin(12, Pin.OUT)
led_2 = Pin(13, Pin.OUT)
button = Pin(27, Pin.IN, Pin.PULL_UP)
low = 250
high = 0


while True:
    lcd.clear()
    distance = sensor.distance_cm()
    if distance < low and distance > 0:
        low = distance
        led_1.value(1)
        time.sleep_ms(500)
        led_1.value(0)
    if distance > high:
        high = distance
        led_2.value(1)
        time.sleep_ms(500)
        led_2.value(0)
    if button.value() == 0:
        print('hello')
        low = 250
        high = 0
        
    lcd.move_to(0,0)
    lcd.putstr('Dis: {:.1f}'.format(distance) + ' cm')
    lcd.move_to(0,1)
    lcd.putstr('H:{:.1f}'.format(high) + ',L:{:.1f}'.format(low))
    time.sleep(1)
    
   

