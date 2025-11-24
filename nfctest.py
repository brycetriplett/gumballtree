import nfc
import time

def on_connect(tag):
    uid = tag.identifier.hex().upper()
    print("Card detected! UID:", uid)
    return True  # disconnect after reading

def main():
    clf = nfc.ContactlessFrontend('usb')
    if not clf:
        print("No NFC reader found")
        return

    print("Waiting for card tap...")
    last_uid = None

    try:
        while True:
            # Wait for a card tap
            clf.connect(rdwr={'on-connect': on_connect})

            # Small delay to avoid multiple prints for the same tap
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nExiting.")
        clf.close()

if __name__ == "__main__":
    main()
