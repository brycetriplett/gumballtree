from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException
import time

def main():
    r = readers()
    if not r:
        print("No readers detected.")
        return

    reader = r[0]  # your single reader
    print("Using:", reader)

    conn = reader.createConnection()
    last_uid = None

    print("Waiting for a card tap...")

    while True:
        try:
            # Try to connect; if no card, exception is raised
            try:
                conn.connect()
            except CardConnectionException:
                time.sleep(0.2)
                continue

            # APDU command to get UID
            GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            data, sw1, sw2 = conn.transmit(GET_UID)

            if sw1 == 0x90 and sw2 == 0x00:
                uid = toHexString(data)
                if uid != last_uid:
                    print("Card detected! UID:", uid)
                    last_uid = uid

            time.sleep(0.2)

        except CardConnectionException:
            # Card removed
            if last_uid is not None:
                print("Card removed.")
                last_uid = None
            time.sleep(0.2)

        except Exception as e:
            print("Error:", e)
            time.sleep(0.2)

if __name__ == "__main__":
    main()
