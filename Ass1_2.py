#Antoine and Mariam
from machine import Pin
import time


#parameters
led_red = Pin(12, Pin.OUT)
led_green = Pin(13, Pin.OUT)
button_1 = Pin(14, Pin.IN, Pin.PULL_UP)
button_2 = Pin(27, Pin.IN, Pin.PULL_UP)
long_press = 300 #ms
correct_password = "SSLS"
password = ""


while True:
    if button_1.value() == 0:
        start = time.ticks_ms()
        
        while button_1.value() == 0:
            time.sleep_ms(10)
            
        duration = time.ticks_diff(time.ticks_ms(), start)
        
        if duration >= long_press:
            password += "L"

        else:
            password += "S"
            
        time.sleep_ms(10)
        
    if button_2.value() == 0:
        time.sleep_ms(100)
        if password == correct_password:
            led_green.value(1)
            time.sleep_ms(500)
            led_green.value(0)
            
        else:
            led_red.value(1)
            time.sleep_ms(500)
            led_red.value(0)
            
        time.sleep_ms(10)
        password = ""