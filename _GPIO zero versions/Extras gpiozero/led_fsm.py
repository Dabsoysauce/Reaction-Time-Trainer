# This program illustrates how to control an LED.
# It uses a finite state machine (FSM).


# General libraries
import time
# Libraries for the GPIO pins
from gpiozero import LED


# Set GPIO Pins
led = LED(16)

# Start with LED off
led.off()


# Initialize the finite state machine
FSM1State = 0
FSM1NextState = 0
FSM1LastTime = 0


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
                led.on()      
                FSM1NextState = 1
            else:
                FSM1NextState = 0

        elif (FSM1State == 1):
            if (currentTime - FSM1LastTime > 0.5):
                print('LED off')
                led.off()       
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
    # Turn off LED
    led.off()
    # Clean up the resources
    led.close()
