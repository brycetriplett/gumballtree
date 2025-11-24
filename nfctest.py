import nfc


def on_connect(tag):
    print("Card detected!")
    print("UID:", tag.identifier.hex())
    return True  # keep the connection alive until the card is removed


def main():
    # Use the PC/SC backend (your working pcscd)
    clf = nfc.ContactlessFrontend('pcsc')
    print("Waiting for NFC card taps...")

    try:
        while True:
            clf.connect(rdwr={'on-connect': on_connect})
    except KeyboardInterrupt:
        print("\nExiting...")
        clf.close()


if __name__ == "__main__":
    main()
