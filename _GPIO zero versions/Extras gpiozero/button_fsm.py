# This program illustrates how to read from a button
# to control an LED.
# It uses a finite state machine (FSM).


# General libraries
import time
# Libraries for the GPIO pins
from gpiozero import LED, Button


# Set GPIO Pins
led = LED(16)
btn = Button(20, pull_up=True)

# Start with LED off
led.off()


# Initialize the finite state machine
FSM1State = 0
FSM1NextState = 0
FSM2State = 0
FSM2NextState = 0


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
            if (btn.is_pressed):
                print("Button was pressed")
                FSM1NextState = 1
            else:
                FSM1NextState = 0

        # State 1: Button is pressed 
        elif (FSM1State == 1):
            if (not btn.is_pressed):
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
                led.on()      
                print("LED on")
                FSM2NextState = 1
            else:
                FSM2NextState = 0
                
        # State 1: Led is on 
        elif (FSM2State == 1):
            if (Toggle):
                led.off()      
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
    # Turn off LED
    led.off()
    # Clean up the resources
    led.close()
    btn.close()


