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


# from pca9685_driver import Device
# import time
#
# # Initialize PCA9685 device at address 0x40 on I2C bus 2
# dev = Device(0x40, 2)
#
# # Set frequency for servos (50 Hz)
# dev.set_pwm_frequency(50)
#
# # Helper: convert pulse width (milliseconds) to 12-bit value (0–4095)
# def pulse_ms_to_val(ms):
#     period_ms = 1000.0 / 50.0   # 20 ms for 50 Hz
#     return int((ms / period_ms) * 4096)
#
# # Servo channel assignments
# servo1_ch = 0   # First servo (existing)
# servo2_ch = 2   # Second servo (DS51150-12V)
#
# # Function to move a servo to a given pulse width
# def move_servo(channel, ms):
#     val = pulse_ms_to_val(ms)
#     dev.set_pwm(channel, val)
#
# # Example motion pattern
# try:
#     while True:
#         # Move both servos in sequence
#         print("Moving both servos to 1.0 ms (min position)")
#         move_servo(servo1_ch, 1.0)
#         move_servo(servo2_ch, 1.0)
#         time.sleep(1)
#
#         print("Moving both servos to 1.5 ms (center)")
#         move_servo(servo1_ch, 1.5)
#         move_servo(servo2_ch, 1.5)
#         time.sleep(1)
#
#         print("Moving both servos to 2.0 ms (max position)")
#         move_servo(servo1_ch, 2.0)
#         move_servo(servo2_ch, 2.0)
#         time.sleep(1)
#
# except KeyboardInterrupt:
#     # Turn off PWM output for safety
#     print("\nStopping servos.")
#     dev.set_pwm(servo1_ch, 0)
#     dev.set_pwm(servo2_ch, 0)
#
