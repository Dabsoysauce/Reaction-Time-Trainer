# This program demonstrates how to control a servo directly
# from the GPIO pins, without the use of a PWM driver.


# General libraries
import time
# Libraries for the harware PWM
import pigpio


# Set GPIO pins for harware PWM
# Note: There are only two hardware PWMs
#         channel 0: pin 12 (but it may make 18 unusable as well)
#         channel 1: pin 19 (but it may make 13 unusable as well)
GPIO_Servo = 19


# Set PWM parameters
pwm_frequency = 50

# Start the hardware pwm service
pi = pigpio.pi()


# Set the duty cycle
def set_duty_cycle(angle):
    duty_min = 2.5 * float(pwm_frequency) / 50.0
    duty_max = 12.5 * float(pwm_frequency) / 50.0
    duty_percent = (duty_max-duty_min)*float(angle)/180.0 + duty_min
    return int(duty_percent/100.0 * 1000000)

# Set the initial angle
angle = 0
pi.hardware_PWM(GPIO_Servo, pwm_frequency, set_duty_cycle(angle))


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
                pi.hardware_PWM(GPIO_Servo, pwm_frequency, set_duty_cycle(angle))
                FSM1NextState = 1
                print ("Move to 45 degrees")
            else:
                FSM1NextState = 0

        # State 1: angle of 45 or on the way there
        elif (FSM1State == 1):      
            if (currentTime - FSM1LastTime > 1):
                angle = 90
                pi.hardware_PWM(GPIO_Servo, pwm_frequency, set_duty_cycle(angle))
                FSM1NextState = 2
                print ("Move to 90 degrees")
            else:
                FSM1NextState = 1

        # State 2: angle of 90 or on the way there
        elif (FSM1State == 2):      
            if (currentTime - FSM1LastTime > 1):
                angle = 135
                pi.hardware_PWM(GPIO_Servo, pwm_frequency, set_duty_cycle(angle))
                FSM1NextState = 3
                print ("Move to 135 degrees")
            else:
                FSM1NextState = 2

        # State 3: angle of 135 or on the way there
        elif (FSM1State == 3):      
            if (currentTime - FSM1LastTime > 1):
                angle = 180
                pi.hardware_PWM(GPIO_Servo, pwm_frequency, set_duty_cycle(angle))
                FSM1NextState = 4
                print ("Move to 180 degrees")
            else:
                FSM1NextState = 3

        # State 4: angle of 180 or on the way there
        elif (FSM1State == 4):      
            if (currentTime - FSM1LastTime > 1):
                angle = 0
                pi.hardware_PWM(GPIO_Servo, pwm_frequency, set_duty_cycle(angle))
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
    # Stop the servo
    pi.hardware_PWM(GPIO_Servo, pwm_frequency, 0)
    pi.stop()
    # Clean up the resources
