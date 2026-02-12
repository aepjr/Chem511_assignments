#assignment 4
#Antoine and Mariam

from machine import Pin, ADC, I2C
import i2c_lcd
import time
from utils import Button, Buzzer, Potentiometer, TimerDisplay, CountdownTimer

#setup

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
lcd = i2c_lcd.I2cLcd(i2c, 0x27, 2, 16)

toggle_btn = Button(26)
start_btn = Button(27)
pot = Potentiometer(32)
alarm = Buzzer(14) 
display = TimerDisplay(lcd)

timer = CountdownTimer(toggle_btn, start_btn, pot, alarm, display)

#code

while True:
    timer.setup_time()
    timer.run_timer()
