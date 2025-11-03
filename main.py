import time
import nfc
from pca9685_driver import Device

# --- Servo setup ---
dev = Device(0x40, 1)
dev.set_pwm_frequency(50)
servo_ch = 0

def pulse_ms_to_val(ms):
    period_ms = 1000.0 / 50.0
    return int((ms / period_ms) * 4096)

def run_servo_motion():
    """Rotate FS90R forward 90°, stop, rotate backward 90°, stop."""
    for ms in (1.25, 1.7, 2.0):  # Forward → stop → Backward → stop
        dev.set_pwm(servo_ch, pulse_ms_to_val(ms))
        time.sleep(0.9)  # same timing as your working test

    # Turn off channel
    dev.set_pwm(servo_ch, 0)

# --- NFC setup ---
clf = nfc.ContactlessFrontend('tty:serial0:pn532')

def on_connect(tag):
    print("Tag detected:", tag)
    run_servo_motion()
    return True

try:
    print("Waiting for NFC tag...")
    while True:
        clf.connect(rdwr={'on-connect': on_connect})
        time.sleep(0.2)
finally:
    clf.close()
