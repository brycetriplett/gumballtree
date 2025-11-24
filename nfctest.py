from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.CardConnection import CardConnection
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
            # Try connecting in DIRECT mode (needed for NFC)
            conn.connect(mode=CardConnection.DIRECT)

            # APDU command to read UID
            GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            data, sw1, sw2 = conn.transmit(GET_UID)

            if sw1 == 0x90 and sw2 == 0x00:
                uid = toHexString(data)
                # Only print if new card tapped
                if uid != last_uid:
                    print("Card detected! UID:", uid)
                    last_uid = uid

            time.sleep(0.2)

        except CardConnectionException:
            # No card present — reset state and wait
            if last_uid is not None:
                print("Card removed.")
                last_uid = None
            time.sleep(0.2)

        except Exception as e:
            # Ignore other exceptions for now
            print("Error:", e)
            time.sleep(0.2)

if __name__ == "__main__":
    main()
