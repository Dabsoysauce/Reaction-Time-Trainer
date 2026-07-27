# This program illustrates how to capture frames in a video stream
# and how to do further processing on them


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
config = camera.create_video_configuration(
    #-----------------------------------------------------
    # Picam natively uses RGB, but OpenCV, which we use for manipulating
    # and displaying images, uses BGR. So we will work with BGR.
    # We can change the settings of picam to give us BGR instead, and
    # we don't need to do an explic conversion. Confusingly, "RGB888"
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
    print("To end the program, press q when hovering over a window")
    print("or press CTRL+C in the terminal.")
    
    # Continuously grab camera frames
    while True:
             
        # Grab a frame
        img = camera.capture_array()
        
        #-----------------------------------------------------
        # We will use numpy to do all our image manipulations
        #-----------------------------------------------------

        # Get the size of the np array
        w,h,d = img.shape
        
        # Make a copy of the image
        img1 = img.copy()

        # Modify the copy of the image 
        img1[w//4:3*w//4 , h//4:3*h//4 , :] = 255 - img1[w//4:3*w//4 , h//4:3*h//4 , :]

        # Show the frames (OpenCV assumes BRG color representation)
        cv2.imshow("Orignal frame", img)
        cv2.imshow("Modified frame", img1)
        
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
