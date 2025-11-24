from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import NoCardException
import time
import requests

ACTIVATE_URL = "http://192.168.137.48:8000/activate"

def main():
    # Get reader
    r = readers()[0]
    print("Using:", r)
    connection = r.createConnection()

    last_uid = None

    while True:
        try:
            # Try connecting to see if a card is present
            connection.connect()

            # APDU command to read UID
            GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            data, sw1, sw2 = connection.transmit(GET_UID)

            if sw1 == 0x90 and sw2 == 0x00:
                uid = toHexString(data)

                # Trigger HTTP GET only when a new card is tapped
                if uid != last_uid:
                    print("Card detected! UID:", uid)
                    try:
                        requests.get(ACTIVATE_URL, timeout=2)
                        print(f"GET request sent to {ACTIVATE_URL}")
                    except requests.RequestException as e:
                        print(f"Failed to send GET request: {e}")
                    last_uid = uid
            else:
                print(f"Error reading UID: {hex(sw1)} {hex(sw2)}")

        except NoCardException:
            # Card removed → reset state and wait again
            if last_uid is not None:
                print("Card removed.")
                last_uid = None

        # Small delay to keep CPU usage low
        time.sleep(0.2)

if __name__ == "__main__":
    main()
