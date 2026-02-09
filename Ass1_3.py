#Antoine and Mariam
from machine import Pin, ADC
import time


led = Pin(13, Pin.OUT)
photodiode = ADC(Pin(34))
photodiode.ATTN_11DB
day_light = 2000



while True:
    if photodiode.read() >= day_light:
        led.value(1)
        
    else:
        led.value(0)