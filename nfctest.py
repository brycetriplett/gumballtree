from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException

def main():
    r = readers()
    if not r:
        print("No readers detected.")
        return

    # Use your reader name exactly
    reader = r[0]
    print("Using:", reader)

    conn = reader.createConnection()

    # Try connection in the only valid NFC mode
    try:
        conn.connect()
    except CardConnectionException:
        # Try direct/raw mode — required for some ACR122U clones
        from smartcard.CardConnection import CardConnection
        conn.connect(mode=CardConnection.DIRECT)

    print("Connected. Waiting for card...")

    GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

    while True:
        try:
            data, sw1, sw2 = conn.transmit(GET_UID)

            if sw1 == 0x90 and sw2 == 0x00:
                print("Card UID:", toHexString(data))
        except Exception:
            # No card present – ignore
            pass


if __name__ == "__main__":
    main()
