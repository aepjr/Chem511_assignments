from machine import I2C, Pin, ADC
import time


class Button:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.last_state = 1

    def is_pressed(self):
        return self.pin.value() == 0

    def was_pressed(self):
        current = self.pin.value() == 0
        pressed = current and self.last_state
        self.last_state = not current
        return pressed
    
  
class Buzzer:
    def __init__(self, pin):
        self.output = Pin(pin, Pin.OUT, value=1)
        self.off()

    def on(self):
        self.output.value(0)

    def off(self):
        self.output.value(1)


class Potentiometer:
    def __init__(self, pin):
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)

    def read_scaled(self, max_value):
        raw = self.adc.read()
        return int((raw / 4095) * max_value)
    
    
class TimerDisplay:
    def __init__(self, lcd):
        self.lcd = lcd
        self.last_minutes = None
        self.last_seconds = None
        self.last_mode = None  # "setting" or "running" or "done"

    def show_setting(self, minutes, seconds):
        if (minutes, seconds) != (self.last_minutes, self.last_seconds) or self.last_mode != "setting":
            self.lcd.clear()
            self.lcd.move_to(0, 0)
            self.lcd.putstr("Set Timer:")
            self.lcd.move_to(0, 1)
            self.lcd.putstr("{:02d}:{:02d}".format(minutes, seconds))
            self.last_minutes = minutes
            self.last_seconds = seconds
            self.last_mode = "setting"

    def show_time(self, minutes, seconds):
        if (minutes, seconds) != (self.last_minutes, self.last_seconds) or self.last_mode != "running":
            self.lcd.clear()
            self.lcd.move_to(0, 0)
            self.lcd.putstr("Time Left:")
            self.lcd.move_to(0, 1)
            self.lcd.putstr("{:02d}:{:02d}".format(minutes, seconds))
            self.last_minutes = minutes
            self.last_seconds = seconds
            self.last_mode = "running"

    def show_done(self):
        if self.last_mode != "done":
            self.lcd.clear()
            self.lcd.move_to(0, 0)
            self.lcd.putstr("Time is Over")
            self.lcd.move_to(0, 1)
            self.lcd.putstr("Death is Iminent")
            self.last_mode = "done"  
  

       
class CountdownTimer:
    def __init__(self, toggle_btn, start_btn, pot, alarm, display):
        self.toggle_btn = toggle_btn
        self.start_btn = start_btn
        self.pot = pot
        self.alarm = alarm
        self.display = display

        self.minutes = 0
        self.seconds = 0
        self.mode = "minutes"  # "minutes" or "seconds"
        self.alarm.off()


    def setup_time(self):
        while True:
          
            value = int(self.pot.read_scaled(59))
            if self.mode == "minutes":
                self.minutes = value
            else:
                self.seconds = value

            self.display.show_setting(self.minutes, self.seconds)

            
            if self.toggle_btn.is_pressed():
                time.sleep(0.3)  
                self.mode = "seconds" if self.mode == "minutes" else "minutes"

           
            if self.start_btn.is_pressed():
                if self.minutes == 0 and self.seconds == 0:
                    continue  
                time.sleep(0.3) 
                break

            time.sleep(0.05)

    
    def run_timer(self):
        total_seconds = self.minutes*60 + self.seconds
        if total_seconds <= 0:
            return

        while total_seconds > 0:
            m = total_seconds // 60
            s = total_seconds % 60
            self.display.show_time(m, s)
            time.sleep(1)
            total_seconds -= 1

        
        self.display.show_done()
        self.alarm.on()

        first_press_done = False

        while True:
            if self.start_btn.is_pressed():
                if not first_press_done:
                    
                    self.alarm.off()
                    first_press_done = True
                    time.sleep(0.3)  
                else:
                    
                    time.sleep(0.3)  
                    break
            time.sleep(0.05)        
        
