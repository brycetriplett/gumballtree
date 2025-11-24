import nfc

def on_connect(tag):
    print("Card detected!")
    print("UID:", tag.identifier.hex())
    return True

clf = nfc.ContactlessFrontend('usb')  # <-- use 'usb' instead of 'pcsc'
print("Waiting for card tap...")

while True:
    clf.connect(rdwr={'on-connect': on_connect})

