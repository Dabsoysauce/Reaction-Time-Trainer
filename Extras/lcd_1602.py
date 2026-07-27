# This program demonstrates how to write to a 16x2 LCD display.
# It uses an HD44780 display driven directly over the GPIO pins
# in 4-bit mode, so no extra libraries are needed.


# General libraries
import time
# Libraries for the GPIO pins
import RPi.GPIO as GPIO


# Connect the display to the following pins
#      LCD pin              RPI
#   1  VSS         to        GND
#   2  VDD         to        5V
#   3  V0          to        middle leg of a 10k potentiometer
#                            (outer legs go to 5V and GND; this sets contrast)
#   4  RS          to        GPIO 26
#   5  RW          to        GND        <-- important, see the warning below
#   6  E           to        GPIO 19
#   7  D0          to        not connected
#   8  D1          to        not connected
#   9  D2          to        not connected
#  10  D3          to        not connected
#  11  D4          to        GPIO 13
#  12  D5          to        GPIO 6
#  13  D6          to        GPIO 5
#  14  D7          to        GPIO 21
#  15  A           to        5V through a 220 ohm resistor (backlight)
#  16  K           to        GND                           (backlight)
#
# WARNING: the display runs at 5V but the GPIO pins are 3.3V and are NOT
# 5V tolerant. Tying RW to GND means the display can only ever be written
# to, never read from, so it never drives 5V back into the Pi. Do not wire
# RW to a GPIO pin unless you are using a level shifter.


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO Pins
LcdRS = 26
LcdE = 19
LcdD4 = 13
LcdD5 = 6
LcdD6 = 5
LcdD7 = 21

# Set GPIO direction (IN / OUT)
GPIO.setup(LcdRS, GPIO.OUT)
GPIO.setup(LcdE, GPIO.OUT)
GPIO.setup(LcdD4, GPIO.OUT)
GPIO.setup(LcdD5, GPIO.OUT)
GPIO.setup(LcdD6, GPIO.OUT)
GPIO.setup(LcdD7, GPIO.OUT)


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


try:
    print("Press CTRL+C to end the program.")

    lcd_init()

    # Write something to both rows
    lcd_string("Hello, world!", LCD_LINE_1)
    lcd_string("SCFC", LCD_LINE_2)
    time.sleep(3)

    # Now count upwards on the second row, to show the display updating.
    # Only the second row is rewritten, so the first row stays put.
    lcd_string("Seconds:", LCD_LINE_1)

    counter = 0
    LastTime = time.time()

    while True:

        # Check the current time
        currentTime = time.time()

        if (currentTime - LastTime > 1.0):
            LastTime = currentTime
            counter = counter + 1

            lcd_string(str(counter), LCD_LINE_2)
            print("Counter is " + str(counter))

        # Small pause so the loop does not hog the processor
        time.sleep(0.01)

# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass
finally:
    # Clean up the resources
    lcd_clear()
    GPIO.cleanup()
