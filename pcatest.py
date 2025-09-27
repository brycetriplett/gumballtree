from pca9685_driver import Device

# Device(address, bus_number)
dev = Device(0x40, 2)   # chip at 0x40 on /dev/i2c-2

# Set frequency (50 Hz for servos, ~1000 Hz for LEDs)
dev.set_pwm_frequency(50)

# Example: sweep servo on channel 0
import time
servo_ch = 0

def pulse_ms_to_val(ms):
    # Convert pulse width (ms) to 0–4095 count (12-bit)
    period_ms = 1000.0 / 50.0   # 20 ms
    return int((ms / period_ms) * 4096)

for ms in (1.0, 1.5, 2.0, 1.5):
    dev.set_pwm(servo_ch, pulse_ms_to_val(ms))
    time.sleep(0.8)

# Turn channel 0 off
dev.set_pwm(servo_ch, 0)
