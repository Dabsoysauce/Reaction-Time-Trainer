# This is a basic program to test the camera
# It shows a single image


# Libraries to control the camera
from picamera2 import Picamera2
import cv2


# Initialize the camera
camera = Picamera2()

try:
    # Start the camera
    camera.start()

    print("To end the program, press any key when hovering over a window")
    print("or press CTRL+C in the terminal.")

    # Grab and show a camera frame
    img = camera.capture_array()
    cv2.imshow("Camera", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            
    # The waitKey command is needed to force openCV to show the image
    # It looks for a keystroke for x ms (with x the argument) and otherwise continues
    # It returns -1 if no key was pressed
    while cv2.waitKey(1) == -1:
        pass
        
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:   
    # Clean up the resources
    cv2.destroyAllWindows()
    camera.stop()
    camera.close()
