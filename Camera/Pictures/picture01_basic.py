# This is a basic program to test the camera
# It takes a picture and stores it in a file


# General libraries
import time
# Libraries to control the camera
from picamera2 import Picamera2


# Initialize the camera
camera = Picamera2()

try:
    print("Program will end automatically (after a few seconds)")
    print("or press CTRL+C in the terminal.")
    
    # Start the camera
    camera.start()

    # Allow the camera to settle before taking an image
    time.sleep(1)

    # Take a picture
    filename = "image_test.jpg"
    camera.capture_file(filename)

    print("Program has finished. Picture stored: " + filename)


# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:   
    # Clean up the resources
    camera.stop()
    camera.close()