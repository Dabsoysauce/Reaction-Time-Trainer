# This program demonstrates how to control a continuous rotation
# servo directly from the GPIO pins, without the use of a PWM driver.


# General libraries
import time
# Libraries for the GPIO pins
import RPi.GPIO as GPIO
 
 
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
# set GPIO Pins
GPIO_Servo = 19

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_Servo, GPIO.OUT)


# Set PWM parameters
pwm_frequency = 50

# Helper function
def set_duty_speed(speed):
    duty_min = 5 * float(pwm_frequency) / 50.0
    duty_max = 10 * float(pwm_frequency) / 50.0
    duty_A = 0.5*(duty_max + duty_min)
    duty_B = 0.5*(duty_max - duty_min)
    return (duty_A + duty_B*float(speed))

# Create a PWM instance
pwm_servo = GPIO.PWM(GPIO_Servo, pwm_frequency)

# Set the speed (between -1 and 1)
pwm_servo.start(0)


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
                speed = 0.5
                pwm_servo.ChangeDutyCycle(set_duty_speed(speed))
                FSM1NextState = 1
                print ("Speed of",speed)
            else:
                FSM1NextState = 0

        # State 1: speed of 0.5
        elif (FSM1State == 1):      
            if (currentTime - FSM1LastTime > 1):
                speed = 1
                pwm_servo.ChangeDutyCycle(set_duty_speed(speed))
                FSM1NextState = 2
                print ("Speed of",speed)
            else:
                FSM1NextState = 1

        # State 2: speed of 1
        elif (FSM1State == 2):      
            if (currentTime - FSM1LastTime > 1):
                speed = 0
                pwm_servo.ChangeDutyCycle(set_duty_speed(speed))
                FSM1NextState = 3
                print ("Speed of",speed)
            else:
                FSM1NextState = 2

        # State 3: speed of -1
        elif (FSM1State == 3):      
            if (currentTime - FSM1LastTime > 1):
                speed = -0.5
                pwm_servo.ChangeDutyCycle(set_duty_speed(speed))
                FSM1NextState = 4
                print ("Speed of",speed)
            else:
                FSM1NextState = 3

        # State 4: speed of -0.5
        elif (FSM1State == 4):      
            if (currentTime - FSM1LastTime > 1):
                speed = -1
                pwm_servo.ChangeDutyCycle(0)        # Clean way to get a full stop
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
    pwm_servo.stop()  
    # Clean up the resources
    GPIO.cleanup()           
