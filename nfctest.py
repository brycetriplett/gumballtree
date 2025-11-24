from smartcard.System import readers
from smartcard.Exceptions import CardConnectionException
from smartcard.scard import SCARD_PROTOCOL_RAW, SCARD_LEAVE_CARD

import time


def main():
    rlist = readers()
    if not rlist:
        print("No smart card readers found")
        return

    reader = rlist[0]
    print(f"Using reader: {reader}")

    while True:
        try:
            connection = reader.createConnection()
            # Use RAW protocol to avoid T0/T1 issues
            connection.connect(protocol=SCARD_PROTOCOL_RAW)

            # APDU to get UID for ISO14443A cards
            GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            data, sw1, sw2 = connection.transmit(GET_UID)

            uid = ''.join(f"{byte:02X}" for byte in data)
            print(f"Card detected! UID: {uid}")

            # Wait for the card to be removed
            while True:
                try:
                    connection.transmit(GET_UID)
                    time.sleep(0.5)
                except CardConnectionException:
                    print("Card removed")
                    break

        except CardConnectionException:
            # No card present, wait a moment
            time.sleep(0.5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(0.5)


if __name__ == "__main__":
    main()

