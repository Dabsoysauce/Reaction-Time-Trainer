# This program demonstrates how to control a servo directly
# from the GPIO pins, without the use of a PWM driver.


# General libraries
import time
# Libraries for the GPIO pins
import RPi.GPIO as GPIO


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
# Set GPIO Pins
GPIO_Servo = 19

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_Servo, GPIO.OUT)


# Set the pwm frequency
pwm_frequency = 50

# Helper function
def set_duty_servo(angle):
    duty_min = 2.5 * float(pwm_frequency) / 50.0
    duty_max = 12.5 * float(pwm_frequency) / 50.0
    return ((duty_max - duty_min) * float(angle) / 180.0 + duty_min)

# Create a PWM instance
pwm_servo = GPIO.PWM(GPIO_Servo, pwm_frequency)

# Start the pwm
angle = 0
pwm_servo.start(set_duty_servo(angle))


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
        # State 0: angle of 0 or on the way there
        if (FSM1State == 0):        
            if (currentTime - FSM1LastTime > 1):
                angle = 45
                pwm_servo.ChangeDutyCycle(set_duty_servo(angle))
                FSM1NextState = 1
                print ("Move to 45 degrees")
            else:
                FSM1NextState = 0

        # State 1: angle of 45 or on the way there
        elif (FSM1State == 1):      
            if (currentTime - FSM1LastTime > 1):
                angle = 90
                pwm_servo.ChangeDutyCycle(set_duty_servo(angle))
                FSM1NextState = 2
                print ("Move to 90 degrees")
            else:
                FSM1NextState = 1

        # State 2: angle of 90 or on the way there
        elif (FSM1State == 2):      
            if (currentTime - FSM1LastTime > 1):
                angle = 135
                pwm_servo.ChangeDutyCycle(set_duty_servo(angle))
                FSM1NextState = 3
                print ("Move to 135 degrees")
            else:
                FSM1NextState = 2

        # State 3: angle of 135 or on the way there
        elif (FSM1State == 3):      
            if (currentTime - FSM1LastTime > 1):
                angle = 180
                pwm_servo.ChangeDutyCycle(set_duty_servo(angle))
                FSM1NextState = 4
                print ("Move to 180 degrees")
            else:
                FSM1NextState = 3

        # State 4: angle of 180 or on the way there
        elif (FSM1State == 4):      
            if (currentTime - FSM1LastTime > 1):
                angle = 0
                pwm_servo.ChangeDutyCycle(set_duty_servo(angle))
                FSM1NextState = 0
                print ("Move to 0 degrees")
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
    # Clean up the resources
    GPIO.cleanup()
