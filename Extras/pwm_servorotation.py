# This program demonstrates the use of the PCA9685 PWM driver.
# This is useful to effectively control multiple servos.
# In this example, there is a continuous rotation servo on channel 2.
# This shows the basic setup without a finite state machine.


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
    

duration = 2

try:
    print("Press CTRL+C to end the program.")
        
    while True:

        channel = channel_rotation1
        speed = 1
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))          
        time.sleep(duration)

        channel = channel_rotation1
        speed = 0.5
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))
        time.sleep(duration)

        channel = channel_rotation1
        speed = 0.35
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))
        time.sleep(duration)

        channel = channel_rotation1
        speed = -1.0
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))
        time.sleep(duration)
        

 
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:
    # Stop the continuous rotation servo
    channel = channel_rotation1
    kit.continuous_servo[channel].throttle = 0
    # Clean up the resources

