# This is a basic program to test the camera
# It shows the camera video stream


# General libraries
import time
# Libraries to control the camera
from picamera2 import Picamera2
import cv2


# Initialize the camera
camera = Picamera2()


try:
    # Start the camera
    camera.start()
    print("To end the program, press q when hovering over a window")
    print("or press CTRL+C in the terminal.")
    
    # Continuously grab camera frames
    while True:
        # Grab a frame
        img = camera.capture_array()
    
        #-----------------------------------------------------
        # Picam natively uses RGB, but OpenCV, which we use for manipulating
        # and displaying images, uses BGR.
        # In this example, we do an explicit conversion from RGB (picamera)
        # to BGR (opencv) in order to display the images properly.
        #-----------------------------------------------------
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        # Show the frame (OpenCV assumes BRG color representation)
        cv2.imshow("Camera", img)
        
        # The waitKey command is needed to force openCV to show the image
        # It looks for a keystroke for x ms (with x the argument) and otherwise continues
        # In this case, the program check if the user pressed 'q'
        if cv2.waitKey(1) == ord('q'):
            break
        
        
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:   
    # Clean up the resources
    cv2.destroyAllWindows()
    camera.stop()
    camera.close()