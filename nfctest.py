import nfc
import time

def on_connect(tag):
    print("Card detected!")
    if hasattr(tag, "identifier"):
        print("UID:", tag.identifier.hex())
    else:
        print(tag)
    return True  # keep connected until removed

def main():
    try:
        clf = nfc.ContactlessFrontend('usb')
    except IOError as e:
        print("Failed to open NFC reader:", e)
        return

    print("Waiting for a card tap...")
    while True:
        try:
            clf.connect(rdwr={'on-connect': on_connect, 'beep-on-connect': True})
        except Exception as e:
            # ignore timeout errors and keep polling
            time.sleep(0.2)

if __name__ == "__main__":
    main()
