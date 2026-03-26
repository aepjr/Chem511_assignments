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
)

led = Pin(13, Pin.OUT)  # change to your LED pin
relay = Pin(27, Pin.OUT)

relay.value(0)

# Replace with YOUR UID (use the one you printed earlier)
AUTHORIZED_UID = [71, 210, 254, 4, 111]

print("Waiting for RFID card...")

# ====== LOOP ======
while True:
    (status, tag_type) = rdr.request(rdr.REQIDL)

    if status == rdr.OK:
        (status, uid) = rdr.anticoll()

        if status == rdr.OK:
            print("Card detected:", uid)

            if uid == AUTHORIZED_UID:
                print("Access granted ✅")
                led.value(1)
                relay.value(1)
                
                time.sleep(5)
                
                led.value(0)
                relay.value(0)
                time.sleep(3)
            else:
                print("Access denied ❌")

            time.sleep(1)  # debounce

    time.sleep(0.1)