# This program illustrates how to run video preview and take images
# when the spacebar is pressed. It also shows how to resize images.


# General libraries
import time
import numpy as np 
# Libraries to control the camera
from picamera2 import Picamera2
from libcamera import Transform
import cv2


# Initialize the camera
camera = Picamera2()

# Configure the camera
# Note that this example uses "create_video_configuration".
# We use this when we capture video or multiple images.
config = camera.create_video_configuration(
    #-----------------------------------------------------
    # Picam natively uses RGB, but OpenCV, which we use for manipulating
    # and displaying images, uses BGR. So we will work with BGR.
    # We can change the settings of picam to give us BGR instead, and
    # we don't need to do an explicit conversion. Confusingly, "RGB888"
    # means that frames will be grabbed BGR format (and vice versa).
    #-----------------------------------------------------
    main = {"size": (640, 480), "format": "RGB888"},
    controls={"FrameRate": 32},
    transform = Transform(rotation = 180)
)
camera.configure(config)


try:
    # Start the camera
    camera.start()
    print("To store a picture, press SPACE when hovering over a window.")
    print("To end the program, press q when hovering over a window")
    print("or press CTRL+C in the terminal.")
    
    # Continuously grab camera frames
    counter = 0
    while True:
        # Grab a frame 
        img = camera.capture_array()

        # Show the frame (OpenCV assumes BRG color representation)
        cv2.imshow("Camera", img)
        
        # The waitKey command is needed to force openCV to show the image
        # It looks for a keystroke for x ms (with x the argument) and otherwise continues
        # In this case, depending on the key stroke it stores a picture or exits the loop
        key = cv2.waitKey(1)
        if key == ord(' '):
            
            # Store the image (with the name including the counter variable)
            filename = "image_%s.jpg" % counter
            camera.capture_file(filename)
            print("Stored: " + filename)
            
            # Also store a resized version of the image
            img_resized = cv2.resize(img, (80,60))
            cv2.imwrite("image_%s_resized.jpg" % counter, img_resized)
            
            counter += 1
        
        elif key == ord('q'):
            break        

        
        
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:   
    # Clean up the resources
    cv2.destroyAllWindows()
    camera.stop()
    camera.close()

