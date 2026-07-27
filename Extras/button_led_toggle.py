# This program turns an LED on and off with a push button.
# One click turns it on, the next click turns it off.
# This is the simple (non-FSM) version of button_fsm.py


# General libraries
import time
# Libraries for the GPIO pins
import RPi.GPIO as GPIO


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO Pins
LedPin = 16
BtnPin = 20

# Set GPIO direction (IN / OUT)
# Set LedPin as output
# Set BtnPin as input, and pull up to high level (3.3V)
GPIO.setup(LedPin, GPIO.OUT)
GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)


# Remember whether the LED is currently on, and start with it off
LedOn = False
GPIO.output(LedPin, GPIO.LOW)


try:
    print("Press CTRL+C to end the program.")

    while True:

        # The button pin reads 0 while the button is being held down
        if (GPIO.input(BtnPin) == 0):

            # Wait until the button is released, so holding it down
            # only counts as a single click
            while (GPIO.input(BtnPin) == 0):
                time.sleep(0.01)

            # Flip the LED to the opposite of what it was
            LedOn = not LedOn

            if (LedOn):
                GPIO.output(LedPin, GPIO.HIGH)
                print("LED on")
            else:
                GPIO.output(LedPin, GPIO.LOW)
                print("LED off")

            # Short pause so the switch bouncing is not read as extra clicks
            time.sleep(0.05)

# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass
finally:
    # Clean up the resources
    GPIO.output(LedPin, GPIO.LOW)
    GPIO.cleanup()
