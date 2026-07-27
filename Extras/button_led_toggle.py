# This program turns an LED on and off with a push button.
# One click turns it on, the next click turns it off.
# This is the simple (non-FSM) version of button_fsm.py


# General libraries
import time
# Libraries for the GPIO pins
import RPi.GPIO as GPIO


# Set this to True to print what the button is doing.
# Set it to False once everything works.
DEBUG = True


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

# Remember what the button read last time round the loop, so we can spot
# the moment it changes instead of reacting the whole time it is held
LastBtn = GPIO.input(BtnPin)
LastChangeTime = 0
DebounceTime = 0.05

# Used by the debug heartbeat below
LastHeartbeat = 0


try:
    print("Press CTRL+C to end the program.")

    if (DEBUG):
        print("DEBUG is on. Idle should read 1, pressed should read 0.")
        print("Button currently reads " + str(LastBtn))

    while True:

        # Check the current time
        currentTime = time.time()

        # Read the button. It reads 0 while it is being held down.
        Btn = GPIO.input(BtnPin)

        # Has the button changed since last time round the loop?
        # The time check ignores the mechanical bouncing of the contacts.
        if (Btn != LastBtn) and (currentTime - LastChangeTime > DebounceTime):

            LastChangeTime = currentTime
            LastBtn = Btn

            if (Btn == 0):
                if (DEBUG):
                    print("Button pressed")

                # Flip the LED to the opposite of what it was
                LedOn = not LedOn

                if (LedOn):
                    GPIO.output(LedPin, GPIO.HIGH)
                    print("LED on")
                else:
                    GPIO.output(LedPin, GPIO.LOW)
                    print("LED off")

            else:
                if (DEBUG):
                    print("Button released")

        # Every second, print the raw pin reading.
        # If this stays at 0 after you let go of the button, the problem is
        # the wiring, not the program.
        if (DEBUG) and (currentTime - LastHeartbeat > 1.0):
            LastHeartbeat = currentTime
            print("  [debug] button pin = " + str(Btn) + ", LedOn = " + str(LedOn))

        # Small pause so the loop does not hog the processor
        time.sleep(0.01)

# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass
finally:
    # Clean up the resources
    GPIO.output(LedPin, GPIO.LOW)
    GPIO.cleanup()
