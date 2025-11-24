import nfc
import time

def on_connect(tag):
    print("Card detected!")
    print(f"UID: {tag.identifier.hex()}")
    return True  # keep connection until card is removed

def main():
    clf = None
    # Retry loop for opening the reader
    while clf is None:
        try:
            print("Trying to open reader...")
            clf = nfc.ContactlessFrontend('pcsc')
        except OSError as e:
            print(f"Reader not ready: {e}. Retrying in 2s...")
            time.sleep(2)

    print("Reader is ready. Waiting for a card tap...")

    # Continuous loop for card detection
    while True:
        try:
            clf.connect(rdwr={'on-connect': on_connect})
        except Exception as e:
            print(f"Error during connect: {e}")
            time.sleep(1)  # short delay before retrying

if __name__ == "__main__":
    main()
