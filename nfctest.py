import nfc


def on_connect(tag):
    print("Card detected!")
    print("UID:", tag.identifier.hex())
    return True  # keep connection until card is removed


def main():
    try:
        # Open PC/SC backend
        clf = nfc.ContactlessFrontend('pcsc')
        print("Waiting for a card tap...")

        while True:
            clf.connect(rdwr={'on-connect': on_connect})

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if clf:
            clf.close()


if __name__ == "__main__":
    main()
