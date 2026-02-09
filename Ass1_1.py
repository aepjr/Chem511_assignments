#Antoine and Mariam
from machine import Pin
import time


#parameters
led_red = Pin(12, Pin.OUT)
led_green = Pin(13, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)
long_press = 500 #ms



while True:
    if button.value() == 0:
        start = time.ticks_ms()
        
        while button.value() == 0:
            time.sleep_ms(10)
            
        duration = time.ticks_diff(time.ticks_ms(), start)
        
        if duration >= long_press:
            led_green.value(1)
            time.sleep_ms(200)
            led_green.value(0)
            print("Long Press")  

        else:
            led_red.value(1)
            time.sleep_ms(200)
            led_red.value(0)
            print("Short Press")
        time.sleep_ms(10)