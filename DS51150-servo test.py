import RPi.GPIO as GPIO
import time

# Set the GPIO pin where your servo is connected
SERVO_PIN = 18  # GPIO18 (PWM capable on Raspberry Pi)

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create PWM instance at 50Hz (standard for servo motors)
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_angle(angle):
    """
    Moves servo to the given angle (0 to 180 degrees).
    Most servos use a duty cycle between 2.5% and 12.5% for 0-180 degrees.
    """
    duty = 2.5 + (angle / 180.0) * 10  # Scale 0-180 to 2.5-12.5
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Optional: to stop signal after move

def stop_servo():
    """
    Stops PWM and cleans up GPIO.
    """
    pwm.stop()
    GPIO.cleanup()
    print("Servo stopped and GPIO cleaned up.")

# ==== TEST ROUTINE ====
try:
    print("Moving to 0°")
    set_angle(0)
    time.sleep(1)

    print("Moving to 90°")
    set_angle(90)
    time.sleep(1)

    print("Moving to 180°")
    set_angle(180)
    time.sleep(1)

    print("Returning to 90°")
    set_angle(90)
    time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    stop_servo()
