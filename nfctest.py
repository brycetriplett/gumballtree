import nfc

try:
    clf = nfc.ContactlessFrontend('usb')
    print("Reader opened successfully!")
except IOError as e:
    print("Failed to open NFC reader:", e)
