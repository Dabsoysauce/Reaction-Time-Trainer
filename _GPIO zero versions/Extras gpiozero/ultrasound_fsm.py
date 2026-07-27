# This program demonstrates how to control an ultrasound distance sensor
#
# Note: The library also has a DistanceSensor class we may consider using


# General libraries
import time
# Libraries for the GPIO pins
from gpiozero import OutputDevice, InputDevice


# set GPIO Pins
TriggerPin  = OutputDevice(18)
EchoPin     = InputDevice(24)
 

# Wait for sensor to settle
TriggerPin.off()
print("Waiting for sensor to settle")
time.sleep(2)
print("Start sensing")


# Helper function to get the distance from the ultrasound sensor.
# It returns the measured distance in cm or -1 if it doesn't detect anything nearby.
# The function can take up to 0.25 seconds to execute.
# The details are not important; you should not modify this code
# --- Start of the ultrasound sensor helper function ---
def distance():
    
    # Create a pulse on the trigger pin
    # This activates the sensor and tells it to send out an ultrasound signal
    TriggerPin.on()
    time.sleep(0.00001)
    TriggerPin.off()

    # Wait for a pulse to start on the echo pin
    # The response is not valid if it takes too long, and we should break the loop
    valid = True
    RefTime = time.time()
    StartTime = RefTime
    while (not EchoPin.is_active) and (StartTime-RefTime < 0.1):
        StartTime = time.time()
    if (StartTime-RefTime >= 0.1):
        valid = False
        
    # Wait for a pulse to end on the echo pin
    # The response is not valid if it takes too long, and we should break the loop
    if (valid):
        RefTime = time.time()
        StopTime = time.time()
        while (EchoPin.is_active) and (StopTime-RefTime < 0.1):
            StopTime = time.time()
        if (StopTime-RefTime >= 0.1):
            valid = False
        
    # If we received a complete pulse on the echo pin (i.e., valid == True)
    # Calculate the distance based on the length of the echo pulse and
    # the speed of sound (34300 cm/s)
    if (valid):
        EchoPulseLength = StopTime - StartTime
        return (EchoPulseLength * 34300) / 2        # Divide by 2 because we are calculating based on a reflection, so the travel time there and back
    else:
        return -1
        
# --- End of the ultrasound sensor helper function ---


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
                dist = distance()
                print("Measured Distance = {0} cm".format(dist))
                FSM1NextState = 0
            else:
                FSM1NextState = 0 

        # State ?? 
        else:
            print("Error: unrecognized state for FSM1")
            noError = False   

         # If there is a state change, record the time    
        if (FSM1State != FSM1NextState):
            FSM1LastTime = currentTime
                
        

# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:
    # Clean up the resources
    TriggerPin.off()
    TriggerPin.close()
    EchoPin.close()
