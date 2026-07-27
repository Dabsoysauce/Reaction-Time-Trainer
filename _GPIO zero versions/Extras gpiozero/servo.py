# This program demonstrates how to control a servo directly
# from the GPIO pins, without the use of a PWM driver.
# This shows the basic setup without a finite state machine.


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


 
try:
    print("Press CTRL+C to end the program.")
        
    while True:
        
        angle = 0
        pi.hardware_PWM(GPIO_Servo, pwm_frequency, set_duty_cycle(angle))
        print ("0")
        time.sleep(1)
        
        angle = 45
        pi.hardware_PWM(GPIO_Servo, pwm_frequency, set_duty_cycle(angle))
        print ("45")
        time.sleep(1)
        
        angle = 90
        pi.hardware_PWM(GPIO_Servo, pwm_frequency, set_duty_cycle(angle))
        print ("90")
        time.sleep(1)

        angle = 135
        pi.hardware_PWM(GPIO_Servo, pwm_frequency, set_duty_cycle(angle))
        print ("135")
        time.sleep(1)

        angle = 180
        pi.hardware_PWM(GPIO_Servo, pwm_frequency, set_duty_cycle(angle))
        print ("180")
        time.sleep(1)
            



# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:
    # Stop the servo
    pi.hardware_PWM(GPIO_Servo, pwm_frequency, 0)
    pi.stop()
    # Clean up the resources

