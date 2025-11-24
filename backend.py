from flask import Flask
from pca9685_driver import Device
from time import sleep

# --- Servo and PCA9685 settings ---
I2C_BUS = 2
I2C_ADDR = 0x40
SERVO_FREQ = 50
SERVO_CH = 2

# Servo pulse specs
MIN_MS = 0.5
MAX_MS = 2.5

# Initialize Flask
api = Flask(__name__)

# --- Servo helper functions ---
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

def spin_servo():
    """Move servo from 0→360→0 smoothly."""
    dev = Device(I2C_ADDR, I2C_BUS)
    dev.set_pwm_frequency(SERVO_FREQ)

    for x in range(0, 361, 3):
        set_servo_angle(dev, x)
        sleep(0.01)

    for x in range(360, -1, -3):
        set_servo_angle(dev, x)
        sleep(0.01)

# --- Flask route ---
@api.route('/activate', methods=['POST', 'GET'])
def activate():
    try:
        spin_servo()
        return "Servo activated", 200
    except Exception as e:
        return f"Error: {e}", 500

# --- Run server ---
if __name__ == "__main__":
    api.run(host='0.0.0.0', port=8000)
