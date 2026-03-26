from machine import Pin
from mfrc522 import MFRC522
import time

# ====== SETUP ======
rdr = MFRC522(
    sck=18,
    mosi=23,
    miso=19,
    rst=22,
    cs=5
) #connecting to the RFID module using the driver found on github

led_red = Pin(13, Pin.OUT)
led_green = Pin(12, Pin.OUT)
led_blue = Pin(14, Pin.OUT) 
relay = Pin(27, Pin.OUT)

relay.value(0)
led_blue.value(1)

# Authorized Fob
AUTHORIZED_UID = [71, 210, 254, 4, 111]

print("Waiting for RFID card...") #for debugging 

# ====== LOOP ======
while True:
    (status, tag_type) = rdr.request(rdr.REQIDL)

    if status == rdr.OK:
        (status, uid) = rdr.anticoll()

        if status == rdr.OK:
            print("Card detected:", uid)

            if uid == AUTHORIZED_UID:
                print("Access granted ✅") #for debugging
                led_blue.value(0)
                led_green.value(1)
                relay.value(1)
                
                time.sleep(5)
                
                led_green.value(0)
                led_blue.value(1)
                relay.value(0)
                time.sleep(3)
            else:
                print("Access denied ❌") #for debugging
                led_blue.value(0)
                led_red.value(1)
                time.sleep(2)
                led_blue.value(1)
                led_red.value(0)

            time.sleep(1)  

    time.sleep(0.1)