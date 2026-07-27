# This program illustrates how to interface with the USB wireless gamepad
# This is a barebones non-blocking implementation.
# It separates button and joystick events (to lower the risk of missing a
# button event when moving a joystick)


# Libraries for the gamepad
from evdev import InputDevice, categorize


# Check if the gamepad is connected
# You need to adjust the event number if the wrong input device is read
#       Method: Unplug the dongle, open a terminal window and list what you see in /dev/input/
#               Now plug in the dongle, and list /dev/input again. You should see an event that
#               was not there before. This is the one you need to use below.
gamepad = InputDevice('/dev/input/event2')
print(gamepad)


try:

    print("Press CTRL+C to end the program.")

    while True:

        # Process the gamepad events
        # This implementation is non-blocking
        newbutton = False
        newstick  = False
        try:
            for event in gamepad.read():            # Use this option (and comment out the next line) to react to the latest event only
            #event = gamepad.read_one()             # Use this option (and comment out the previous line) when you don't want to miss any event
                eventinfo = categorize(event)
                if event.type == 1:
                    newbutton = True
                    codebutton  = eventinfo.scancode
                    valuebutton = eventinfo.keystate
                elif event.type == 3:
                    newstick = True
                    codestick  = eventinfo.event.code
                    valuestick = eventinfo.event.value
        except:
            pass

        # If there was a gamepad event, show it
        if newbutton:
            print("Button: ",codebutton,valuebutton)
        if newstick:
            print("Stick : ",codestick,valuestick)



# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:
    # Clean up the resources
    gamepad.close()
        

