from mfrc522 import MFRC522
import time

rdr = MFRC522(
    sck=18,
    mosi=23,
    miso=19,
    rst=22,
    cs=5
)
print("Test reg:", rdr._rreg(0x37))
print("Waiting for RFID card...")

while True:
    (status, tag_type) = rdr.request(rdr.REQIDL)

    if status == rdr.OK:
        print("Card detected (request stage)")

        (status, uid) = rdr.anticoll()

        if status == rdr.OK:
            print("UID:", uid)
        else:
            print("Anticollision failed")

    else:
        print("No card")

    time.sleep(0.5)