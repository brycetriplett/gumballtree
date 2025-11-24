from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.scard import SCARD_PROTOCOL_T1
from smartcard.Exceptions import CardConnectionException
import time

class NFCObserver(CardObserver):
    def update(self, observable, actions):
        added_cards, removed_cards = actions

        for card in added_cards:
            print("Card detected!")
            try:
                connection = card.createConnection()
                connection.connect()  # auto protocol
                GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
                data, sw1, sw2 = connection.transmit(GET_UID)
                print(f"SW1: {sw1:02X}, SW2: {sw2:02X}")  # DEBUG
                if sw1 == 0x90 and sw2 == 0x00:
                    uid = ''.join(f'{b:02X}' for b in data)
                    print("UID:", uid)
                else:
                    print("Card responded but no UID returned.")
            except Exception as e:
                print("Failed to read card:", e)

        for card in removed_cards:
            print("Card removed.")


def main():
    print("Waiting for cards... (Ctrl+C to exit)")
    monitor = CardMonitor()
    observer = NFCObserver()
    monitor.addObserver(observer)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        monitor.deleteObserver(observer)

if __name__ == "__main__":
    main()

