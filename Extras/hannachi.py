# HANNACHI - a whack a mole game.
#
# Four servos each hold up a mole. One mole pops up at random, and you have
# to hit the button on that mole before the time runs out. You get a point
# for each mole you hit in time, and the game lasts 10 rounds.
#
# The game gets harder or easier depending on how well you did, and you can
# keep playing again without restarting the program.


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
# Connect each mole's servo signal wire (orange or white) to
#     Mole                   RPI
#   mole 1 servo        to   GPIO 12 (physical pin 32)
#   mole 2 servo        to   GPIO 16 (physical pin 36)
#   mole 3 servo        to   GPIO 18 (physical pin 12)
#   mole 4 servo        to   GPIO 17 (physical pin 11)
#
# Connect each mole's button. One leg goes to the GPIO pin below, and the
# diagonally opposite leg goes to the ground rail.
#     Mole                   RPI
#   mole 1 button       to   GPIO 25 (physical pin 22)
#   mole 2 button       to   GPIO 24 (physical pin 18)
#   mole 3 button       to   GPIO 23 (physical pin 16)
#   mole 4 button       to   GPIO 22 (physical pin 15)
#
# GPIO 20 is deliberately not used, because that pin is broken on our Pi.
#
# GROUND RAIL: with four servos, four buttons and a display there are too
# many ground wires to put one per pin. Run a wire from a Pi ground pin
# (physical pin 6 and physical pin 39 are both ground) to the long ground
# rail down the side of the breadboard, and take every ground connection
# from that rail.
#
# SERVO POWER - READ THIS: do not run four servos from the Pi's own 5V pin.
# Four servos starting to move at once pull far more current than the Pi
# can supply, and the Pi will either reset or the display will fill with
# rubbish. Use a separate 5V supply for the servo power wires (red), rated
# for at least 2A. The separate supply's ground MUST be joined to the Pi's
# ground rail as well, or the servos and the Pi will not agree on what the
# signal wires are doing.
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

# Set GPIO Pins for the display
LcdRS = 26
LcdE = 19
LcdD4 = 13
LcdD5 = 6
LcdD6 = 5
LcdD7 = 21

# Each entry is one mole: its name, its servo pin, and its button pin.
# To add a fifth mole, wire it up and add one line here.
Moles = [
    ("Mole 1", 12, 25),
    ("Mole 2", 16, 24),
    ("Mole 3", 18, 23),
    ("Mole 4", 17, 22),
]

# Set GPIO direction (IN / OUT)
GPIO.setup(LcdRS, GPIO.OUT)
GPIO.setup(LcdE, GPIO.OUT)
GPIO.setup(LcdD4, GPIO.OUT)
GPIO.setup(LcdD5, GPIO.OUT)
GPIO.setup(LcdD6, GPIO.OUT)
GPIO.setup(LcdD7, GPIO.OUT)

for name, servoPin, buttonPin in Moles:
    # The servo signal pin is an output
    GPIO.setup(servoPin, GPIO.OUT)
    # The button pin is an input, pulled up to high level (3.3V)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)


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

# The two angles each mole moves between
ANGLE_DOWN = 0
ANGLE_UP = 85

# How long to allow for a servo to travel, in seconds
MOVE_TIME = 0.4

# How many rounds one game lasts
TOTAL_ROUNDS = 10

# How long the player gets to hit the mole at the start, in seconds.
# This goes up or down between games depending on how well they did.
START_TIME_LIMIT = 1.0

# If the score is this or lower, the game gets easier
EASIER_SCORE = 4
EASIER_TIME_LIMIT = 1.5

# If the score is this or higher, the game gets harder
HARDER_SCORE = 8
HARDER_TIME_LIMIT = 0.5

# Set the pwm frequency
pwm_frequency = 50


# Helper function
def set_duty_servo(angle):
    duty_min = 2.5 * float(pwm_frequency) / 50.0
    duty_max = 12.5 * float(pwm_frequency) / 50.0
    return ((duty_max - duty_min) * float(angle) / 180.0 + duty_min)


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


def set_mole(index, angle):
    # Tell one mole's servo to go to an angle. This returns straight away;
    # the servo carries on moving in the background while the program gets
    # on with reading the buttons.
    pwm_servos[index].ChangeDutyCycle(set_duty_servo(angle))


def all_moles_down():
    # Put every mole back down
    for i in range(len(Moles)):
        set_mole(i, ANGLE_DOWN)
    time.sleep(MOVE_TIME)


def wait_for_hit(timeout):
    # Wait until one of the buttons is pressed, and return which mole it
    # belonged to along with how long the player took.
    # If timeout is greater than zero and nothing is pressed in that time,
    # give up and return -1. A timeout of zero means wait forever.

    startTime = time.time()

    # Read the buttons first, so that a button which is already being held
    # down does not count. We are looking for the moment a pin changes from
    # high to low, not for it simply being low.
    LastState = []
    for name, servoPin, buttonPin in Moles:
        LastState.append(GPIO.input(buttonPin))

    while True:
        elapsed = time.time() - startTime

        # Has the player run out of time?
        if (timeout > 0) and (elapsed > timeout):
            return -1, elapsed

        # Check every button in turn
        for i in range(len(Moles)):
            buttonPin = Moles[i][2]
            state = GPIO.input(buttonPin)

            # Has this button just gone from released to pressed?
            if (state == 0) and (LastState[i] == 1):
                return i, elapsed

            LastState[i] = state

        # Small pause so the loop does not hog the processor
        time.sleep(0.005)


def play_game(timeLimit):
    # Play one whole game of TOTAL_ROUNDS rounds, and return the score

    score = 0

    for roundNumber in range(1, TOTAL_ROUNDS + 1):

        # Put every mole down and wait a random moment, so the player
        # cannot guess when the next mole is coming
        all_moles_down()

        lcd_string("Round " + str(roundNumber) + " of " + str(TOTAL_ROUNDS), LCD_LINE_1)
        lcd_string("Get ready...", LCD_LINE_2)
        time.sleep(random.uniform(0.5, 2.0))

        # Pick a mole at random and send it up
        target = random.randint(0, len(Moles) - 1)
        print("Round " + str(roundNumber) + ": " + Moles[target][0] + " is up")

        lcd_string("HIT IT!", LCD_LINE_1)
        lcd_string("Score: " + str(score), LCD_LINE_2)
        set_mole(target, ANGLE_UP)

        # The clock starts as soon as the mole begins to rise, and the
        # buttons are read while it is still moving, so an early hit
        # still counts
        hit, reactionTime = wait_for_hit(timeLimit)

        # The round is over either way, so put the mole back down
        set_mole(target, ANGLE_DOWN)

        if (hit == -1):
            lcd_string("TOO SLOW!", LCD_LINE_1)
            print("Too slow. Score is still " + str(score))
        elif (hit == target):
            score = score + 1
            lcd_string("HIT! " + str(round(reactionTime, 2)) + "s", LCD_LINE_1)
            print("Hit in " + str(round(reactionTime, 2)) + "s. Score is now " + str(score))
        else:
            lcd_string("WRONG MOLE!", LCD_LINE_1)
            print("Wrong, that was " + Moles[hit][0] + ". Score is still " + str(score))

        lcd_string("Score: " + str(score), LCD_LINE_2)

        # Hold the result on screen long enough to read it. This also gives
        # the button contacts time to stop bouncing before the next round.
        time.sleep(1.5)

    return score


def new_time_limit(score, timeLimit):
    # Work out how long the player should get next game, based on how
    # well they just did

    if (score <= EASIER_SCORE):
        return EASIER_TIME_LIMIT
    elif (score >= HARDER_SCORE):
        return HARDER_TIME_LIMIT
    else:
        # A middling score, so leave the time limit alone
        return timeLimit


# Create a PWM instance for each mole's servo, and start them all down
pwm_servos = []
for name, servoPin, buttonPin in Moles:
    pwm = GPIO.PWM(servoPin, pwm_frequency)
    pwm.start(set_duty_servo(ANGLE_DOWN))
    pwm_servos.append(pwm)


try:
    print("Press CTRL+C to end the program.")

    lcd_init()

    # Introduce the game
    lcd_string("HANNACHI", LCD_LINE_1)
    lcd_string("Whack the moles!", LCD_LINE_2)
    time.sleep(2.5)

    lcd_string("A mole pops up.", LCD_LINE_1)
    lcd_string("Hit its button!", LCD_LINE_2)
    time.sleep(2.5)

    lcd_string(str(TOTAL_ROUNDS) + " rounds. Be", LCD_LINE_1)
    lcd_string("quick about it!", LCD_LINE_2)
    time.sleep(2.5)

    all_moles_down()

    timeLimit = START_TIME_LIMIT

    # Keep playing games until the player gives up and presses CTRL + C
    while True:

        lcd_string("You get " + str(timeLimit) + "s", LCD_LINE_1)
        lcd_string("per mole. Go!", LCD_LINE_2)
        print("Starting a game with a time limit of " + str(timeLimit) + "s")
        time.sleep(2.5)

        score = play_game(timeLimit)

        # Show how they did
        all_moles_down()
        lcd_string("Final score", LCD_LINE_1)
        lcd_string(str(score) + " out of " + str(TOTAL_ROUNDS), LCD_LINE_2)
        print("Final score: " + str(score) + " out of " + str(TOTAL_ROUNDS))
        time.sleep(3)

        # Make the next game easier or harder to suit the player
        oldTimeLimit = timeLimit
        timeLimit = new_time_limit(score, timeLimit)

        if (timeLimit > oldTimeLimit):
            lcd_string("Slowing it down", LCD_LINE_1)
        elif (timeLimit < oldTimeLimit):
            lcd_string("Speeding it up!", LCD_LINE_1)
        else:
            lcd_string("Nicely done", LCD_LINE_1)

        lcd_string("Now " + str(timeLimit) + "s per mole", LCD_LINE_2)
        print("The time limit is now " + str(timeLimit) + "s")
        time.sleep(3)

        # Offer another game. Any button starts it.
        lcd_string("Play again?", LCD_LINE_1)
        lcd_string("Hit any mole!", LCD_LINE_2)
        print("Hit any button to play again, or press CTRL+C to stop.")

        # A timeout of zero means wait here for as long as it takes
        wait_for_hit(0)

# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass
finally:
    # Clean up the resources
    lcd_clear()
    for pwm in pwm_servos:
        pwm.stop()
    GPIO.cleanup()
