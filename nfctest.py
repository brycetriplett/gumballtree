from smartcard.System import readers
from smartcard.util import toHexString

r = readers()
reader = [x for x in r if "PICC" in str(x) and "Interface 0" in str(x)][0]
print("Using:", reader)

conn = reader.createConnection()
conn.connect()

print("Waiting for card...")

while True:
    try:
        apdu = [0xFF, 0xCA, 0x00, 0x00, 0x00]  # Get UID
        data, sw1, sw2 = conn.transmit(apdu)

        if sw1 == 0x90:
            print("Card detected:", toHexString(data))
        # loop will continue and print once per tap

    except Exception:
        # no card present
        pass
