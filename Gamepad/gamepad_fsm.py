# This program illustrates how to interface with the USB wireless gamepad
# This is non-blocking, using a finite state machine (FSM).
# It separates button and joystick events (to lower the risk of missing a
# button event when moving a joystick)


# General libraries
import time
# Libraries for the gamepad
from evdev import InputDevice, categorize


# Check if the gamepad is connected
# You need to adjust the event number if the wrong input device is read
#       Method: Unplug the dongle, open a terminal window and list what you see in /dev/input/
#               Now plug in the dongle, and list /dev/input again. You should see an event that
#               was not there before. This is the one you need to use below.
gamepad = InputDevice('/dev/input/event2')
print(gamepad)


# Initialize the finite state machine
FSM1State = 0
FSM1NextState = 0
FSM1LastTime = time.time()
timeoutval = 4

try:

    print("Press CTRL+C to end the program.\n")
    print ("FSM1: go to state 0 (wait for button A press)")

    while True:

        # Check the current time
        currentTime = time.time()

        # Update the state
        FSM1State = FSM1NextState
        
        # Process the gamepad events
        # This implementation is non-blocking
        newbutton = False
        newstick  = False
        try:
            for event in gamepad.read():            # Use this option (and comment out the next line) to react to the latest event only
                #event = gamepad.read_one()         # Use this option (and comment out the previous line) when you don't want to miss any event
                eventinfo = categorize(event)
                if event.type == 1:
                    newbutton = True
                    codebutton  = eventinfo.scancode
                    valuebutton = eventinfo.keystate
                elif event.type == 3:
                    newstick = True
                    codestick  = eventinfo.event.code
                    valuestick = eventinfo.event.value
        except KeyboardInterrupt:
            raise
        except:
            pass


        # State 0:
        if (FSM1State == 0):
            # If button A is pressed
            if (newbutton and codebutton == 305 and valuebutton == 1):                         
                print (" ** Button A was pressed **\n")
                FSM1NextState = 1
                FSM1LastTime = currentTime
                print ("FSM1: go to state 1 (wait for stick pressed down)")
            elif (currentTime - FSM1LastTime > timeoutval):
                print (" ** Time out **\n")
                FSM1NextState = 2
                FSM1LastTime = currentTime
                print ("FSM1: go to state 2 (wait for any button press)")
            else:
                FSM1NextState = 0

        # State 1: 
        elif (FSM1State == 1):
            # If stick is pressed down
            if (newstick and codestick == 1 and valuestick > 200):                         
                print (" ** Stick was pressed down **\n")
                FSM1NextState = 2
                FSM1LastTime = currentTime
                print ("FSM1: go to state 2 (wait for any button press)")                
            elif (currentTime - FSM1LastTime > timeoutval):
                print (" ** Time out **\n")
                FSM1NextState = 0
                FSM1LastTime = currentTime
                print ("FSM1: go to state 0 (wait for button A press)")
            else:
                FSM1NextState = 1
                
        # State 2: 
        elif (FSM1State == 2):
            if (newbutton and valuebutton == 1):
                print (" ** Random button was pressed **\n")
                FSM1NextState = 0
                FSM1LastTime = currentTime
                print ("FSM1: go to state 0 (wait for button A press)")
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
    gamepad.close()

        

