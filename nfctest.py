from smartcard.System import readers
from smartcard.Exceptions import NoCardException
import time

GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]  # ACS ACR122U command

def main():
    r = readers()
    if not r:
        print("No readers found")
        return

    reader = r[0]
    print("Using reader:", reader)

    connection = reader.createConnection()

    last_uid = None

    while True:
        try:
            connection.connect()  # auto protocol
            data, sw1, sw2 = connection.transmit(GET_UID)
            if sw1 == 0x90 and sw2 == 0x00:
                uid = ''.join(f'{b:02X}' for b in data)
                if uid != last_uid:
                    print("Card detected! UID:", uid)
                    last_uid = uid
            else:
                # card present but UID read failed
                last_uid = None
        except NoCardException:
            last_uid = None
        except Exception as e:
            # other errors, ignore and retry
            last_uid = None

        time.sleep(0.3)

if __name__ == "__main__":
    main()
