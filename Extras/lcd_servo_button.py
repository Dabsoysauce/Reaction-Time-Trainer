# This program controls a servo with two buttons and reports what it is
# doing on a 16x2 LCD display.
# The servo starts at 0 degrees. Pressing the red button sends it to 85
# degrees, and pressing the yellow button brings it back down to 0.


# General libraries
import time
# Libraries for the GPIO pins
import RPi.GPIO as GPIO


# Connect the display to the following pins
#      LCD pin              RPI
#   1  VSS         to        GND
#   2  VDD         to        5V
#   3  V0          to        middle leg of a 10k potentiometer
#   4  RS          to        GPIO 26 (physical pin 37)
#   5  RW          to        GND
#   6  E           to        GPIO 19 (physical pin 35)
#  11  D4          to        GPIO 13 (physical pin 33)
#  12  D5          to        GPIO 6  (physical pin 31)
#  13  D6          to        GPIO 5  (physical pin 29)
#  14  D7          to        GPIO 21 (physical pin 40)
#  15  A           to        5V through a 220 ohm resistor
#  16  K           to        GND
#
# Connect the two buttons to the following pins
#     Button                 RPI
#   red, one leg         to  GPIO 25 (physical pin 22)
#   red, diagonal leg    to  GND     (physical pin 20)
#   yellow, one leg      to  GPIO 20 (physical pin 38)
#   yellow, diagonal leg to  GND     (physical pin 39)
#
# Connect the servo to the following pins
#     Servo wire           Colour          RPI
#   signal            orange or white   GPIO 12 (physical pin 32)
#   power             red               5V      (physical pin 2)
#   ground            brown or black    GND     (physical pin 6)
#
# NOTE: servo.py in this folder drives a servo on GPIO 19, but GPIO 19 is
# the display's enable pin here, so this program uses GPIO 12 instead.
#
# POWER WARNING: a servo pulls a large gulp of current each time it starts
# moving. A small servo such as an SG90 will usually run from the Pi's own
# 5V pin, but a larger one, or a servo under load, can drag the supply down
# far enough to reset the Pi. If the Pi reboots when the servo moves, or
# the display fills with rubbish, power the servo from its own 5V supply
# instead. If you do that, the servo's ground and the Pi's ground must
# still be joined together, or the Pi and the servo will not agree on what
# the signal wire is doing.
#
# The two legs of each button must be diagonally opposite each other. The
# legs along each side of a tactile switch are joined together inside the
# switch, so using two from the same side leaves it permanently closed.
#
# No resistors are needed for the buttons. The internal pull-ups hold the
# pins high, and pressing a button pulls its pin down to ground.
#
# The GPIO numbers above are BCM numbers, because this program calls
# GPIO.setmode(GPIO.BCM). They are NOT the same as counting along the
# header. Use the physical pin numbers in brackets to find them.


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO Pins
LcdRS = 26
LcdE = 19
LcdD4 = 13
LcdD5 = 6
LcdD6 = 5
LcdD7 = 21
BtnRed = 25
BtnYellow = 20
GPIO_Servo = 12

# Set GPIO direction (IN / OUT)
GPIO.setup(LcdRS, GPIO.OUT)
GPIO.setup(LcdE, GPIO.OUT)
GPIO.setup(LcdD4, GPIO.OUT)
GPIO.setup(LcdD5, GPIO.OUT)
GPIO.setup(LcdD6, GPIO.OUT)
GPIO.setup(LcdD7, GPIO.OUT)
GPIO.setup(GPIO_Servo, GPIO.OUT)

# Set the button pins as inputs, and pull them up to high level (3.3V)
GPIO.setup(BtnRed, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(BtnYellow, GPIO.IN, pull_up_down = GPIO.PUD_UP)


# The display treats a byte as a command when RS is low,
# and as a character to print when RS is high
LCD_COMMAND = GPIO.LOW
LCD_CHARACTER = GPIO.HIGH

# Where each row starts in the display's memory
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

# How many characters fit on one row
LCD_WIDTH = 16

# How long to hold the enable pin, in seconds
E_PULSE = 0.0005
E_DELAY = 0.0005

# The two angles the servo moves between
ANGLE_DOWN = 0
ANGLE_UP = 85

# How long to allow for the servo to travel, in seconds
MOVE_TIME = 0.6

# Once the servo has arrived, stop sending it pulses. This stops the
# buzzing and stops it drawing current while it is just sitting there.
# Set this to False if the servo has something pushing against it and
# needs to hold its position firmly.
RELEASE_AFTER_MOVE = True

# Set the pwm frequency
pwm_frequency = 50

# The two states the program can be in
STATE_DOWN = 0          # servo is at 0 degrees, waiting for the red button
STATE_UP = 1            # servo is at 85 degrees, waiting for the yellow button


# Helper function
def set_duty_servo(angle):
    duty_min = 2.5 * float(pwm_frequency) / 50.0
    duty_max = 12.5 * float(pwm_frequency) / 50.0
    return ((duty_max - duty_min) * float(angle) / 180.0 + duty_min)


def move_servo(angle):
    # Send the servo to an angle, wait for it to get there, and then
    # optionally stop the pulses so it goes quiet
    pwm_servo.ChangeDutyCycle(set_duty_servo(angle))
    time.sleep(MOVE_TIME)

    if (RELEASE_AFTER_MOVE):
        pwm_servo.ChangeDutyCycle(0)


def lcd_toggle_enable():
    # The display reads the data pins on the falling edge of the enable pin,
    # so we pulse it high then low after setting the data pins
    time.sleep(E_DELAY)
    GPIO.output(LcdE, GPIO.HIGH)
    time.sleep(E_PULSE)
    GPIO.output(LcdE, GPIO.LOW)
    time.sleep(E_DELAY)


def lcd_send_byte(bits, mode):
    # In 4-bit mode we only have four data wires, so each byte is sent as
    # two halves: the high four bits first, then the low four bits

    GPIO.output(LcdRS, mode)

    # High nibble
    GPIO.output(LcdD4, (bits & 0x10) == 0x10)
    GPIO.output(LcdD5, (bits & 0x20) == 0x20)
    GPIO.output(LcdD6, (bits & 0x40) == 0x40)
    GPIO.output(LcdD7, (bits & 0x80) == 0x80)
    lcd_toggle_enable()

    # Low nibble
    GPIO.output(LcdD4, (bits & 0x01) == 0x01)
    GPIO.output(LcdD5, (bits & 0x02) == 0x02)
    GPIO.output(LcdD6, (bits & 0x04) == 0x04)
    GPIO.output(LcdD7, (bits & 0x08) == 0x08)
    lcd_toggle_enable()


def lcd_init():
    # The display needs time to settle after power is applied before it
    # will accept any commands
    time.sleep(0.05)

    # This wake up sequence is what the HD44780 datasheet asks for
    lcd_send_byte(0x33, LCD_COMMAND)        # Initialise
    time.sleep(0.005)
    lcd_send_byte(0x32, LCD_COMMAND)        # Switch to 4-bit mode
    time.sleep(0.005)
    lcd_send_byte(0x28, LCD_COMMAND)        # Two lines, 5x8 dot characters
    lcd_send_byte(0x0C, LCD_COMMAND)        # Display on, cursor off
    lcd_send_byte(0x06, LCD_COMMAND)        # Move the cursor right after typing
    lcd_send_byte(0x01, LCD_COMMAND)        # Clear the display
    time.sleep(E_DELAY)


def lcd_clear():
    lcd_send_byte(0x01, LCD_COMMAND)
    time.sleep(E_DELAY)


def lcd_string(message, line):
    # Pad the message out with spaces so it overwrites whatever
    # was on that row before
    message = message.ljust(LCD_WIDTH, " ")

    # Move the cursor to the start of the row we want
    lcd_send_byte(line, LCD_COMMAND)

    # Then send the characters one at a time
    for i in range(LCD_WIDTH):
        lcd_send_byte(ord(message[i]), LCD_CHARACTER)


# Create a PWM instance
pwm_servo = GPIO.PWM(GPIO_Servo, pwm_frequency)

# Start the pwm
pwm_servo.start(set_duty_servo(ANGLE_DOWN))


try:
    print("Press CTRL+C to end the program.")

    lcd_init()

    # Send the servo to its starting position
    lcd_string("Starting up...", LCD_LINE_1)
    lcd_string("Servo to 0 deg", LCD_LINE_2)
    print("Moving the servo to " + str(ANGLE_DOWN) + " degrees")
    move_servo(ANGLE_DOWN)

    state = STATE_DOWN
    lcd_string("Servo at 0 deg", LCD_LINE_1)
    lcd_string("Press RED", LCD_LINE_2)

    # Remember what the buttons read last time round the loop, so we can spot
    # the moment one changes instead of reacting the whole time it is held
    LastRed = GPIO.input(BtnRed)
    LastYellow = GPIO.input(BtnYellow)
    LastChangeTime = 0
    DebounceTime = 0.05

    while True:

        # Check the current time
        currentTime = time.time()

        # Read the buttons. They read 0 while they are being held down.
        Red = GPIO.input(BtnRed)
        Yellow = GPIO.input(BtnYellow)

        RedPressed = False
        YellowPressed = False

        # Has either button just gone from released to pressed?
        # The time check ignores the mechanical bouncing of the contacts.
        if (currentTime - LastChangeTime > DebounceTime):

            if (Red == 0) and (LastRed == 1):
                RedPressed = True
                LastChangeTime = currentTime
                LastRed = Red

            if (Yellow == 0) and (LastYellow == 1):
                YellowPressed = True
                LastChangeTime = currentTime
                LastYellow = Yellow

        # Keep track of the buttons being let go of
        if (Red == 1):
            LastRed = 1
        if (Yellow == 1):
            LastYellow = 1

        # State 0: the servo is down at 0 degrees, so the red button
        # is the one that does something
        if (state == STATE_DOWN):
            if (RedPressed):
                print("Red pressed, moving to " + str(ANGLE_UP) + " degrees")
                lcd_string("RED pressed", LCD_LINE_1)
                lcd_string("Moving to 85...", LCD_LINE_2)

                move_servo(ANGLE_UP)
                state = STATE_UP

                lcd_string("Servo at 85 deg", LCD_LINE_1)
                lcd_string("Press YELLOW", LCD_LINE_2)

        # State 1: the servo is up at 85 degrees, so the yellow button
        # is the one that does something
        elif (state == STATE_UP):
            if (YellowPressed):
                print("Yellow pressed, moving to " + str(ANGLE_DOWN) + " degrees")
                lcd_string("YELLOW pressed", LCD_LINE_1)
                lcd_string("Moving to 0...", LCD_LINE_2)

                move_servo(ANGLE_DOWN)
                state = STATE_DOWN

                lcd_string("Servo at 0 deg", LCD_LINE_1)
                lcd_string("Press RED", LCD_LINE_2)

        # State ??
        else:
            print("Error: unrecognized state")
            break

        # Small pause so the loop does not hog the processor
        time.sleep(0.01)

# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass
finally:
    # Clean up the resources
    lcd_clear()
    pwm_servo.stop()
    GPIO.cleanup()
