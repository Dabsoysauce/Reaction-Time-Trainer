# This program demonstrates how to control a servo directly
# from the GPIO pins, without the use of a PWM driver.
# This shows the basic setup without a finite state machine.


# General libraries
import time
# Libraries for the GPIO pins
import RPi.GPIO as GPIO


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
# Set GPIO Pins
GPIO_Servo = 19

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_Servo, GPIO.OUT)


# Set the pwm frequency
pwm_frequency = 50

# Helper function
def set_duty_servo(angle):
    duty_min = 2.5 * float(pwm_frequency) / 50.0
    duty_max = 12.5 * float(pwm_frequency) / 50.0
    return ((duty_max - duty_min) * float(angle) / 180.0 + duty_min)

# Create a PWM instance
pwm_servo = GPIO.PWM(GPIO_Servo, pwm_frequency)

# Start the pwm
angle = 0
pwm_servo.start(set_duty_servo(angle))


 
try:
    print("Press CTRL+C to end the program.")
        
    while True:
        
        angle = 0
        pwm_servo.ChangeDutyCycle(set_duty_servo(angle))
        print ("0")
        time.sleep(1)
        
        angle = 45
        pwm_servo.ChangeDutyCycle(set_duty_servo(angle))
        print ("45")
        time.sleep(1)
        
        angle = 90
        pwm_servo.ChangeDutyCycle(set_duty_servo(angle))
        print ("90")
        time.sleep(1)

        angle = 135
        pwm_servo.ChangeDutyCycle(set_duty_servo(angle))
        print ("135")
        time.sleep(1)

        angle = 180
        pwm_servo.ChangeDutyCycle(set_duty_servo(angle))
        print ("180")
        time.sleep(1)
            



# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:
    # Clean up the resources
    GPIO.cleanup()
