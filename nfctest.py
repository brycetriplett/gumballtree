from smartcard.System import readers
from smartcard.Exceptions import NoCardException

r = readers()
if not r:
    print("No readers available")
    exit()

reader = r[0]
print("Using reader:", reader)

connection = reader.createConnection()

while True:
    try:
        connection.connect()  # waits for card
        atr = connection.getATR()
        print("Card ATR:", [hex(x) for x in atr])
        # optionally, send APDU commands here
    except NoCardException:
        # No card, just wait a bit
        import time
        time.sleep(0.5)
