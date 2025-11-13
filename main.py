# #!/usr/bin/env python3
# """
# Servo control demo for PCA9685.
# Moves two servos in 90° increments in a single direction, wrapping around.
# Includes retry logic and safety handling for OSError 16 (I2C busy).
# """
#
# from pca9685_driver import Device
# import time
# import errno
# import sys
#
# # ------------------------------------------------------------
# # CONFIGURATION
# # ------------------------------------------------------------
# I2C_BUS = 2        # /dev/i2c-2
# I2C_ADDR = 0x40    # PCA9685 default address
# SERVO_FREQ = 50    # Hz, typical for hobby servos
#
# # Servo channels
# SERVO1_CH = 0
# SERVO2_CH = 2
#
# # Servo angle limits
# SERVO_MIN_ANGLE = 0
# SERVO_MAX_ANGLE = 180
# ANGLE_STEP = 90     # degrees per step
# STEP_DELAY = 1.0    # seconds between steps
#
# # Pulse width range (ms)
# SERVO_MIN_MS = 1.0
# SERVO_MAX_MS = 2.0
#
#
# # ------------------------------------------------------------
# # HELPER FUNCTIONS
# # ------------------------------------------------------------
# def angle_to_ms(angle, min_ms=SERVO_MIN_MS, max_ms=SERVO_MAX_MS, max_angle=180.0):
#     """Convert desired angle (0–max_angle) to pulse width in ms."""
#     angle = max(0, min(angle, max_angle))  # clamp to range
#     return min_ms + (angle / max_angle) * (max_ms - min_ms)
#
#
# def pulse_ms_to_val(ms):
#     """Convert pulse width in ms to 0–4095 value for PCA9685."""
#     period_ms = 1000.0 / SERVO_FREQ
#     return int((ms / period_ms) * 4096)
#
#
# def safe_set_pwm(dev, ch, val, retries=3, delay=0.05):
#     """Set PWM with retries on I2C busy errors."""
#     for _ in range(retries):
#         try:
#             dev.set_pwm(ch, val)
#             return
#         except OSError as e:
#             if e.errno == errno.EBUSY or e.errno == 16:
#                 time.sleep(delay)
#                 continue
#             raise
#     raise OSError("I2C bus remained busy after retries")
#
#
# # ------------------------------------------------------------
# # MAIN PROGRAM
# # ------------------------------------------------------------
# def main():
#     print("Initializing PCA9685...")
#     dev = Device(I2C_ADDR, I2C_BUS)
#     dev.set_pwm_frequency(SERVO_FREQ)
#     print(f"PCA9685 ready on bus {I2C_BUS} @ 0x{I2C_ADDR:02X}")
#
#     servo1_angle = SERVO_MIN_ANGLE
#     servo2_angle = SERVO_MIN_ANGLE
#
#     try:
#         while True:
#             # Move Servo 1
#             servo1_angle = (servo1_angle + ANGLE_STEP) % (SERVO_MAX_ANGLE + 1)
#             ms1 = angle_to_ms(servo1_angle)
#             safe_set_pwm(dev, SERVO1_CH, pulse_ms_to_val(ms1))
#             print(f"Servo 1 → {servo1_angle}°")
#
#             # Move Servo 2
#             servo2_angle = (servo2_angle + ANGLE_STEP) % (SERVO_MAX_ANGLE + 1)
#             ms2 = angle_to_ms(servo2_angle)
#             safe_set_pwm(dev, SERVO2_CH, pulse_ms_to_val(ms2))
#             print(f"Servo 2 → {servo2_angle}°")
#
#             time.sleep(STEP_DELAY)
#
#     except KeyboardInterrupt:
#         print("\nStopping servos and releasing channels...")
#         safe_set_pwm(dev, SERVO1_CH, 0)
#         safe_set_pwm(dev, SERVO2_CH, 0)
#         print("Done.")
#         sys.exit(0)
#
#
# if __name__ == "__main__":
#     main()


#!/usr/bin/env python3
"""
Spin a 360° servo on PCA9685 once, then stop.
Servo spec: 0.5–2.5ms pulse @ 50Hz, 0–360° range.
"""
#
# #!/usr/bin/env python3
# """
# Spin a 360° servo on PCA9685 once, then stop.
# Servo spec: 0.5–2.5ms pulse @ 50Hz, 0–360° range.
# """
#
# from pca9685_driver import Device
# import time
#
# # ------------------------------------------------------------
# # CONFIGURATION
# # ------------------------------------------------------------
# I2C_BUS = 2          # /dev/i2c-2
# I2C_ADDR = 0x40      # PCA9685 default address
# SERVO_FREQ = 50      # Hz
# SERVO_CH = 2         # Channel for 360° servo
#
# # Pulse width limits for 360° servo
# MIN_MS = 0.5
# MAX_MS = 2.5
#
# # ------------------------------------------------------------
# # HELPER FUNCTIONS
# # ------------------------------------------------------------
# def ms_to_val(ms):
#     """Convert pulse width (ms) to PCA9685 value (0–4095)."""
#     period_ms = 1000.0 / SERVO_FREQ
#     return int((ms / period_ms) * 4096)
#
#
# def set_angle(dev, angle):
#     """Convert angle (0–360) to pulse and send to servo."""
#     angle = max(0, min(angle, 360))
#     ms = MIN_MS + (angle / 360.0) * (MAX_MS - MIN_MS)
#     val = ms_to_val(ms)
#     dev.set_pwm(SERVO_CH, val)
#
#
# # ------------------------------------------------------------
# # MAIN
# # ------------------------------------------------------------
# def main():
#     print("Initializing PCA9685...")
#     dev = Device(I2C_ADDR, I2C_BUS)
#     dev.set_pwm_frequency(SERVO_FREQ)
#     print("Starting 360° rotation...")
#
#     # Sweep from 0 → 360°
#     for angle in range(0, 361, 3):  # step size matches 3° precision
#         set_angle(dev, angle)
#         time.sleep(1)
#
#     # Stop sending signal (optional — depends on servo type)
#     dev.set_pwm(SERVO_CH, 0)
#     print("Rotation complete. Servo stopped.")
#
#
# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
"""
Set 360° positional servo to 0° position on PCA9685.
"""

from pca9685_driver import Device
from time import sleep

I2C_BUS = 2
I2C_ADDR = 0x40
SERVO_FREQ = 50
SERVO_CH = 2

# Servo specs
MIN_MS = 0.5
MAX_MS = 2.5

def ms_to_val(ms):
    """Convert pulse width in ms to PCA9685 value (0–4095)."""
    period_ms = 1000.0 / SERVO_FREQ
    return int((ms / period_ms) * 4096)

def set_servo_angle(dev, angle):
    """Set servo to specific angle (0–360°)."""
    angle = max(0, min(angle, 360))
    ms = MIN_MS + (angle / 360.0) * (MAX_MS - MIN_MS)
    val = ms_to_val(ms)
    dev.set_pwm(SERVO_CH, val)

def main():
    print("Initializing PCA9685...")
    dev = Device(I2C_ADDR, I2C_BUS)
    dev.set_pwm_frequency(SERVO_FREQ)

    print("Setting servo to 0°...")
    set_servo_angle(dev, 0)

    for x in range(-360, 361, 3):
        set_servo_angle(dev, x)
        sleep(0.1)

    set_servo_angle(dev, 0)

    print("Servo positioned at 0°.")

if __name__ == "__main__":
    main()
