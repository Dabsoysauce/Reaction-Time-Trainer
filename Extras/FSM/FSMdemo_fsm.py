# Illustration of a finite state machine (FSM)
# Functionality: print information for the user
#      Note: This is a Mealy-style FSM


# General libraries
import time
 

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
        # This is a Mealy FSM
        # State 0:
        if (FSM1State == 0):
            if (currentTime - FSM1LastTime > 0.7):
                print (" ** Hello **")
                FSM1NextState = 1
                FSM1LastTime = currentTime
                print ("FSM1: go to state 1")
            else:
                FSM1NextState = 0

        # State 1: 
        elif (FSM1State == 1):
            if (currentTime - FSM1LastTime > 0.4):
                print (" ** How are you? **")
                FSM1NextState = 2
                FSM1LastTime = currentTime
                print ("FSM1: go to state 2")
            else:
                FSM1NextState = 1

        # State 2: 
        elif (FSM1State == 2):
            if (currentTime - FSM1LastTime > 1.0):
                print (" ** What's up? **")               
                FSM1NextState = 0
                FSM1LastTime = currentTime
                print ("FSM1: go to state 0")
            else:
                FSM1NextState = 2

        # Unrecognized state
        else:
            print("Error: unrecognized state for FSM1")
            break   


            
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:
    # Clean up the resources
    pass
