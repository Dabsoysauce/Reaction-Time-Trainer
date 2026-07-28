# This program is a reaction game for a 16x2 LCD display and four buttons.
# The display asks for a colour, and you have to press the matching button
# within one second. You get a point for each correct press that is quick
# enough, and the game lasts 10 rounds.


# General libraries
import time
import random
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
# Connect the four buttons to the following pins
#     Button                 RPI
#   yellow, one leg      to  GPIO 20 (physical pin 38)
#   yellow, diagonal leg to  GND     (physical pin 39)
#   blue, one leg        to  GPIO 16 (physical pin 36)
#   blue, diagonal leg   to  GND     (physical pin 34)
#   green, one leg       to  GPIO 12 (physical pin 32)
#   green, diagonal leg  to  GND     (physical pin 30)
#   red, one leg         to  GPIO 25 (physical pin 22)
#   red, diagonal leg    to  GND     (physical pin 20)
#
# The yellow and blue buttons do not move. Each new button follows the same
# pattern as the first two: one leg in a GPIO pin, and the diagonal leg in
# the ground pin next door to it.
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

# Each entry pairs a colour with the pin that button is wired to.
# To add another button, wire it up and add one line here.
Buttons = [
    ("YELLOW", 20),
    ("BLUE", 16),
    ("GREEN", 12),
    ("RED", 25),
]

# Set GPIO direction (IN / OUT)
GPIO.setup(LcdRS, GPIO.OUT)
GPIO.setup(LcdE, GPIO.OUT)
GPIO.setup(LcdD4, GPIO.OUT)
GPIO.setup(LcdD5, GPIO.OUT)
GPIO.setup(LcdD6, GPIO.OUT)
GPIO.setup(LcdD7, GPIO.OUT)

# Set every button pin as an input, and pull it up to high level (3.3V)
for colour, pin in Buttons:
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)


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

# How many rounds the game lasts
TOTAL_ROUNDS = 10

# How long the player has to press the button, in seconds.
# A press after this does not count, even if it is the right button.
TIME_LIMIT = 1.0


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


def wait_for_press(timeout):
    # Wait until one of the buttons is pressed, and return its colour.
    # If nothing is pressed within timeout seconds, give up and return an
    # empty string instead.

    startTime = time.time()

    # Read the buttons first, so that a button which is already being held
    # down when the round starts does not count. We are looking for the
    # moment a pin changes from high to low, not for it simply being low.
    LastState = {}
    for colour, pin in Buttons:
        LastState[colour] = GPIO.input(pin)

    while True:
        # Has the player run out of time?
        if (time.time() - startTime > timeout):
            return ""

        # Check every button in turn
        for colour, pin in Buttons:
            state = GPIO.input(pin)

            # Has this button just gone from released to pressed?
            if (state == 0) and (LastState[colour] == 1):
                return colour

            LastState[colour] = state

        # Small pause so the loop does not hog the processor
        time.sleep(0.01)


try:
    print("Press CTRL+C to end the program.")

    lcd_init()

    lcd_string("Colour game!", LCD_LINE_1)
    lcd_string("Get ready...", LCD_LINE_2)
    time.sleep(2)

    lcd_string("You have " + str(TIME_LIMIT) + "s", LCD_LINE_1)
    lcd_string("for each round", LCD_LINE_2)
    time.sleep(2)

    score = 0

    for roundNumber in range(1, TOTAL_ROUNDS + 1):

        # Pick one of the colours at random for this round
        target = random.choice(Buttons)[0]

        lcd_string("Round " + str(roundNumber) + " of " + str(TOTAL_ROUNDS), LCD_LINE_1)
        lcd_string("Press " + target, LCD_LINE_2)
        print("Round " + str(roundNumber) + ": press " + target)

        # Wait here until the player presses one of the buttons, or until
        # they run out of time. Note the time just before we start waiting,
        # so we can work out how quick they were.
        startTime = time.time()
        pressed = wait_for_press(TIME_LIMIT)
        reactionTime = time.time() - startTime

        # The round is over either way, whether they were right, wrong,
        # or too slow
        if (pressed == ""):
            lcd_string("TOO SLOW!", LCD_LINE_1)
            print("Too slow. Score is still " + str(score))
        elif (pressed == target):
            score = score + 1
            lcd_string("Correct! " + str(round(reactionTime, 2)) + "s", LCD_LINE_1)
            print("Correct in " + str(round(reactionTime, 2)) + "s. Score is now " + str(score))
        else:
            lcd_string("WRONG!", LCD_LINE_1)
            print("Wrong, that was " + pressed + ". Score is still " + str(score))

        lcd_string("Score: " + str(score), LCD_LINE_2)

        # Hold the result on screen long enough to read it. This also gives
        # the button contacts time to stop bouncing before the next round.
        time.sleep(1.5)

    # The game is over, so show the final score
    lcd_string("Final score", LCD_LINE_1)
    lcd_string(str(score) + " out of " + str(TOTAL_ROUNDS), LCD_LINE_2)
    print("Final score: " + str(score) + " out of " + str(TOTAL_ROUNDS))

    # Leave the score on the display until CTRL + C is pressed
    while True:
        time.sleep(0.1)

# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass
finally:
    # Clean up the resources
    lcd_clear()
    GPIO.cleanup()
