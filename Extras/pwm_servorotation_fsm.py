# This program demonstrates the use of the PCA9685 PWM driver.
# This is useful to effectively control multiple servos.
# In this example, there is a continuous rotation servo on channel 2. 


# General libraries
import time
# Libraries for the PWM driver with servos (uses BCM numbering)
from adafruit_servokit import ServoKit


# Specify the channels you are using on the PWM driver
channel_rotation1 = 2


# Initialize ServoKit for the PWA board.
# This automatically fixes the pwm frequency to 50
kit = ServoKit(channels=16)

# This is to control a continuous rotation servo
# It does not work for a DC motor
kit.continuous_servo[channel_rotation1].set_pulse_width_range(1200,1800)
    

# Initialize the finite state machine
FSM1State = 0
FSM1NextState = 0
FSM1LastTime = 0

duration = 2

try:
    print("Press CTRL+C to end the program.")
        
    while True:

        # Check the current time
        currentTime = time.time()

        # Update the state
        FSM1State = FSM1NextState


        # Check the state transitions for FSM 1
        # State 0: angle of 0 on channel 0 or on the way there
        if (FSM1State == 0):        
            if (currentTime - FSM1LastTime > duration):
                channel = channel_rotation1
                speed = 1
                kit.continuous_servo[channel].throttle = speed
                print ('speed: {0} \t channel: {1}'.format(speed,channel))
                FSM1NextState = 1
            else:
                FSM1NextState = 0

        # State 1: angle of 45 on channel 0 or on the way there
        elif (FSM1State == 1):      
            if (currentTime - FSM1LastTime > duration):
                channel = channel_rotation1
                speed = -1
                kit.continuous_servo[channel].throttle = speed
                print ('speed: {0} \t channel: {1}'.format(speed,channel))
                FSM1NextState = 2
            else:
                FSM1NextState = 1

        # State 2: angle of 90 on channel 1 or on the way there
        elif (FSM1State == 2):      
            if (currentTime - FSM1LastTime > duration):
                channel = channel_rotation1
                speed = 0
                kit.continuous_servo[channel].throttle = speed
                print ('speed: {0} \t channel: {1}'.format(speed,channel))
                FSM1NextState = 3
            else:
                FSM1NextState = 2

        # State 3: angle of 135 on channel 0 or on the way there
        elif (FSM1State == 3):      
            if (currentTime - FSM1LastTime > duration):
                channel = channel_rotation1
                speed = 0.4
                kit.continuous_servo[channel].throttle = speed
                print ('speed: {0} \t channel: {1}'.format(speed,channel))
                FSM1NextState = 4
            else:
                FSM1NextState = 3

        # State 4: angle of 180  on channel 1 or on the way there
        elif (FSM1State == 4):      
            if (currentTime - FSM1LastTime > duration):
                channel = channel_rotation1
                speed = -0.2
                kit.continuous_servo[channel].throttle = speed
                print ('speed: {0} \t channel: {1}'.format(speed,channel))
                FSM1NextState = 0
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
    channel = channel_rotation1
    kit.continuous_servo[channel].throttle = 0
    # Clean up the resources

