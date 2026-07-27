# This program demonstrates the use of the PCA9685 PWM driver.
# This is useful to effectively control multiple servos.
# In this example, there is a standard servo on channel 0 and
# a continuous rotation servo(on channel 2). You can also test
# this code with only one of the two channels in use (just don't
# connect anything to the other channel).
# This shows the basic setup without a finite state machine.


# General libraries
import time
# Libraries for the PWM driver with servos (uses BCM numbering)
from adafruit_servokit import ServoKit


# Specify the channels you are using on the PWM driver
channel_servo1 = 0
channel_rotation1 = 2


# Initialize ServoKit for the PWA board.
# This automatically fixes the pwm frequency to 50
kit = ServoKit(channels=16)

# To set the servo range to 180 degrees
# You can adjust the values if needed
kit.servo[channel_servo1].set_pulse_width_range(400,2300)

# This is to control a continuous rotation servo
# It does not work for a DC motor
kit.continuous_servo[channel_rotation1].set_pulse_width_range(1200,1800)
    

duration = 2

try:
    print("Press CTRL+C to end the program.")
        
    while True:

        channel = channel_servo1
        angle = 0
        kit.servo[channel].angle = angle
        print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
        channel = channel_rotation1
        speed = 1
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))
                
        time.sleep(duration)


        channel = channel_servo1
        angle = 180
        kit.servo[channel].angle = angle
        print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
        channel = channel_rotation1
        speed = 0.5
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))
        
        time.sleep(duration)


        channel = channel_servo1
        angle = 90
        kit.servo[channel].angle = angle
        print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
        channel = channel_rotation1
        speed = 0.35
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))
        
        time.sleep(duration)


        channel = channel_servo1
        angle = 135
        kit.servo[channel].angle = angle
        print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
        channel = channel_rotation1
        speed = -1.0
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))
        
        time.sleep(duration)
        

 
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:
    # Stop the servo
    channel = channel_servo1
    kit.servo[channel].angle = None
    # Stop the continuous rotation servo
    channel = channel_rotation1
    kit.continuous_servo[channel].throttle = 0
    # Clean up the resources

