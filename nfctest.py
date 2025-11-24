from smartcard.System import readers
from smartcard.Exceptions import NoCardException

r = readers()
if len(r) == 0:
    print("No readers available")
    exit()

reader = r[0]
print(f"Using reader: {reader}")

while True:
    connection = reader.createConnection()
    try:
        connection.connect()  # will raise NoCardException if no card
        atr = connection.getATR()
        print(f"Card detected! ATR: {atr}")
    except NoCardException:
        pass  # just wait
