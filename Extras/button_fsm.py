# This program illustrates how to read from a button
# to control an LED.
# It uses a finite state machine (FSM).


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


# Initialize the finite state machine
FSM1State = 0
FSM1NextState = 0
FSM2State = 0
FSM2NextState = 0
GPIO.output(LedPin, GPIO.LOW)                                   # Set LedPin low to turn the led off 


try:
    print("Press CTRL+C to end the program.")
        
    while True:

        # Update the state
        FSM1State = FSM1NextState
        FSM2State = FSM2NextState

        Toggle = False
        
        # Check the state transitions for FSM 1
        # State 0: Button is not pressed 
        if (FSM1State == 0):
            if (GPIO.input(BtnPin)== 0):
                print("Button was pressed")
                FSM1NextState = 1
            else:
                FSM1NextState = 0

        # State 1: Button is pressed 
        elif (FSM1State == 1):
            if (GPIO.input(BtnPin)== 1):
                print("Button was released")
                Toggle = True
                FSM1NextState = 0
            else:
                FSM1NextState = 1

        # State ?? 
        else:
            print("Error: unrecognized state for FSM1")
            break


        # Check the state transitions for FSM 2
        # State 0: Led is off 
        if (FSM2State == 0):
            if (Toggle):
                GPIO.output(LedPin, GPIO.HIGH)
                print("LED on")
                FSM2NextState = 1
            else:
                FSM2NextState = 0
                
        # State 1: Led is on 
        elif (FSM2State == 1):
            if (Toggle):
                GPIO.output(LedPin, GPIO.LOW)
                print("LED off")
                FSM2NextState = 0
            else:
                FSM2NextState = 1

        # State ?? 
        else:
            print("Error: unrecognized state for FSM1")
            break  

# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:
    # Clean up the resources
    GPIO.output(LedPin, GPIO.LOW) 
    GPIO.cleanup()


