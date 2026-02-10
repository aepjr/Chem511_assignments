from machine import Pin, ADC, I2C
import time
import i2c_lcd   # your provided class file

# ---------------- BUTTON CLASS ----------------
class Button:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)

    def is_pressed(self):
        return self.pin.value() == 0

# ---------------- POTENTIOMETER CLASS ----------------
class Potentiometer:
    def __init__(self, pin):
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)

    def read_scaled(self, max_value):
        raw = self.adc.read()
        return int((raw / 4095) * max_value)

# ---------------- ALARM CLASS ----------------
class Alarm:
    def __init__(self, pin):
        self.output = Pin(pin, Pin.OUT)

    def on(self):
        self.output.value(1)

    def off(self):
        self.output.value(0)

# ---------------- LCD DISPLAY CLASS ----------------
class TimerDisplay:
    def __init__(self, lcd):
        self.lcd = lcd

    def show_setting(self, mode, value):
        self.lcd.clear()
        self.lcd.putstr("Set " + mode)
        self.lcd.move_to(0,1)
        self.lcd.putstr(str(value))

    def show_time(self, m, s):
        self.lcd.clear()
        self.lcd.putstr("Time Left:")
        self.lcd.move_to(0,1)
        self.lcd.putstr("{:02d}:{:02d}".format(m,s))

    def show_done(self):
        self.lcd.clear()
        self.lcd.putstr("Time Finished!")

# ---------------- MAIN TIMER CLASS ----------------
class CountdownTimer:
    def __init__(self, toggle_btn, start_btn, pot, alarm, display):
        self.toggle_btn = toggle_btn
        self.start_btn = start_btn
        self.pot = pot
        self.alarm = alarm
        self.display = display

        self.minutes = 0
        self.seconds = 0
        self.mode = "minutes"

    def setup_time(self):
        while True:
            value = self.pot.read_scaled(59)

            if self.mode == "minutes":
                self.minutes = value
            else:
                self.seconds = value

            self.display.show_setting(self.mode, value)

            if self.toggle_btn.is_pressed():
                time.sleep(0.3)
                self.mode = "seconds" if self.mode == "minutes" else "minutes"

            if self.start_btn.is_pressed():
                time.sleep(0.3)
                break

            time.sleep(0.1)

    def run_timer(self):
        total_seconds = self.minutes*60 + self.seconds

        while total_seconds > 0:
            m = total_seconds // 60
            s = total_seconds % 60

            self.display.show_time(m,s)
            time.sleep(1)
            total_seconds -= 1

        self.display.show_done()
        self.alarm.on()

        while not self.start_btn.is_pressed():
            time.sleep(0.1)

        self.alarm.off()

# ---------------- HARDWARE SETUP ----------------
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
lcd = i2c_lcd.I2cLcd(i2c, 0x27, 2, 16)

toggle_btn = Button(26)
start_btn = Button(27)
pot = Potentiometer(32)
alarm = Alarm(12)
display = TimerDisplay(lcd)

timer = CountdownTimer(toggle_btn, start_btn, pot, alarm, display)

# ---------------- MAIN LOOP ----------------
while True:
    timer.setup_time()
    timer.run_timer()
