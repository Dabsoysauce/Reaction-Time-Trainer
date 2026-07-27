# This program demonstrates how to control a continuous rotation
# servo directly from the GPIO pins, without the use of a PWM driver.


# General libraries
import time
# Libraries for the harware PWM
import pigpio


# Set GPIO pins for harware PWM
# Note: There are only two hardware PWMs
#         channel 0: pin 12 (but it may make 18 unusable as well)
#         channel 1: pin 19 (but it may make 13 unusable as well)
GPIO_Servo = 19


# Set the pwm frequency is set automatically to 50

# Start the hardware pwm service
pi = pigpio.pi()

# Helper function
# Pulse width in microseconds.
#    Full forward: 2000us, full reverse: 1000us
def widthHWpwm_rot(speed):
    if speed == 0:
        return 0
    pmin = 1000
    pmax = 2000
    return int(0.5*(pmin+pmax) + 0.5*(pmax-pmin)*float(speed))



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
        # State 0: speed of -0
        if (FSM1State == 0):        
            if (currentTime - FSM1LastTime > 1):
                speed = -1
                pi.set_servo_pulsewidth(GPIO_Servo, widthHWpwm_rot(speed))
                FSM1NextState = 1
                print ("Speed of",speed)
            else:
                FSM1NextState = 0

        # State 1: speed of 0.5
        elif (FSM1State == 1):      
            if (currentTime - FSM1LastTime > 1):
                speed = 0
                pi.set_servo_pulsewidth(GPIO_Servo, widthHWpwm_rot(speed))
                FSM1NextState = 2
                print ("Speed of",speed)
            else:
                FSM1NextState = 1

        # State 2: speed of 1
        elif (FSM1State == 2):      
            if (currentTime - FSM1LastTime > 1):
                speed = 1
                pi.set_servo_pulsewidth(GPIO_Servo, widthHWpwm_rot(speed))
                FSM1NextState = 3
                print ("Speed of",speed)
            else:
                FSM1NextState = 2

        # State 3: speed of -1
        elif (FSM1State == 3):      
            if (currentTime - FSM1LastTime > 1):
                speed = 0.35
                pi.set_servo_pulsewidth(GPIO_Servo, widthHWpwm_rot(speed))
                FSM1NextState = 4
                print ("Speed of",speed)
            else:
                FSM1NextState = 3

        # State 4: speed of -0.5
        elif (FSM1State == 4):      
            if (currentTime - FSM1LastTime > 1):
                speed = 0
                pi.set_servo_pulsewidth(GPIO_Servo, widthHWpwm_rot(speed))
                FSM1NextState = 0
                print ("Speed of",speed)
            else:
                FSM1NextState = 4
                
        # State ??
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
    # Stop the continuous rotation servo
    pi.set_servo_pulsewidth(GPIO_Servo, 0)
    pi.stop()
    # Clean up the resources
