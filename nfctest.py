import nfc

def on_connect(tag):
    print("Tag detected!")
    print(tag)
    return True  # keep connection until removed

def main():
    clf = nfc.ContactlessFrontend('usb')
    if not clf:
        print("Failed to open reader")
        return

    print("Waiting for a card tap...")
    while True:
        clf.connect(rdwr={'on-connect': on_connect})

if __name__ == "__main__":
    main()
