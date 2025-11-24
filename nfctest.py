#!/usr/bin/env python3
import nfc
import datetime

def on_connect(tag):
    """Callback when a card is tapped."""
    print("Card detected!")
    print(f"Timestamp: {datetime.datetime.now()}")
    print(f"Tag info: {tag}")
    if hasattr(tag, 'identifier'):
        uid = ''.join(f'{b:02X}' for b in tag.identifier)
        print(f"UID: {uid}")
    print("-" * 30)
    return True  # Keep tag connected until removed

def main():
    # Use the USB backend for ACR122U
    try:
        clf = nfc.ContactlessFrontend('usb')
    except IOError as e:
        print(f"Failed to open reader: {e}")
        return

    print("Waiting for card taps...")
    while True:
        # Wait for a card; calls on_connect when detected
        clf.connect(rdwr={'on-connect': on_connect})

if __name__ == "__main__":
    main()
