# This program illustrates how to control an LED.
# It uses a finite state machine (FSM).


# General libraries
import time
# Libraries for the GPIO pins
import RPi.GPIO as GPIO


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO Pins
LedPin = 16

# Set GPIO direction (IN / OUT)
# Set LedPin as output
GPIO.setup(LedPin, GPIO.OUT)                    

# Initialize the finite state machine
FSM1State = 0
FSM1NextState = 0
FSM1LastTime = 0
GPIO.output(LedPin, GPIO.LOW) 


try:
    print("Press CTRL+C to end the program.")
        
    while True:

        # Check the current time
        currentTime = time.time()

        # Update the state
        FSM1State = FSM1NextState
        
        # Check the state transitions for FSM 1
        if (FSM1State == 0):
            if (currentTime - FSM1LastTime > 0.5):
                print('LED on')
                GPIO.output(LedPin, GPIO.HIGH)      
                FSM1NextState = 1
            else:
                FSM1NextState = 0

        elif (FSM1State == 1):
            if (currentTime - FSM1LastTime > 0.5):
                print('LED off')
                GPIO.output(LedPin, GPIO.LOW)       
                FSM1NextState = 0
            else:
                FSM1NextState = 1

        else:
            print("Error: unrecognized state for FSM1")
            break
            
        # If there is a state change, record the time    
        if (FSM1State != FSM1NextState):
            FSM1LastTime = currentTime
                
               
               
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:
    # Clean up the resources
    GPIO.output(LedPin, GPIO.LOW) 
    GPIO.cleanup()
