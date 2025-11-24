import nfc

def on_connect(tag):
    print("Card detected!")
    print(f"UID: {tag.identifier.hex()}")
    return True  # keep connection until card is removed

def main():
    # Use PCSC backend
    clf = nfc.ContactlessFrontend('pcsc')
    if not clf:
        print("Failed to open reader")
        return

    print("Waiting for a card tap...")
    while True:
        clf.connect(rdwr={'on-connect': on_connect})

if __name__ == "__main__":
    main()

