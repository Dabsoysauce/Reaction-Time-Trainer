# This program illustrates how to capture a single image and
# how to do further processing on it. It also shows how to combine
# multiple images into a 2x2 grid when displaying it.


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
# Note that this example uses "create_still_configuration" instead of "create_video_configuration"
# This is optional. We can use it when we take a single image as it optimizes the quality
# for one-shot capture rather than repeated images (like in video).
config = camera.create_still_configuration(
    #-----------------------------------------------------
    # Picam natively uses RGB, but OpenCV, which we use for manipulating
    # and displaying images, uses BGR. So we will work with BGR.
    # We can change the settings of picam to give us BGR instead, and
    # we don't need to do an explic conversion. Confusingly, "RGB888"
    # means that frames will be grabbed BGR format (and vice versa).
    #-----------------------------------------------------
    main = {"size": (640, 480), "format": "RGB888"},  
    transform = Transform(hflip = False, vflip = False)
)
camera.configure(config)


try:
    # Start the camera
    camera.start()
    print("To end the program, press q when hovering over a window")
    print("or press CTRL+C in the terminal.")
     
    # Allow the camera to settle before taking an image
    time.sleep(1)
            
    # Grab a frame
    img = camera.capture_array()
        

    #-----------------------------------------------------
    # We will use numpy to do all our image manipulations
    #-----------------------------------------------------

    # Get the size of the np array
    w,h,d = img.shape

    # Convert from BGR to RGB, using OpenCV
    # This will look wrong, but it is done to show this command
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
    # We create a separate copy of the numpy array because we don't
    # want to modify the original image
    img2 = img.copy()

    # We only create an alias for the image. So the change we make
    # here will affect both images.
    img3 = img2
    img3[w//4:3*w//4 , h//4:3*h//4 , :] = 0
            
    # Combine the four images into one larger image in a 2x2 grid      
    img_grid = np.vstack(( np.hstack((img,img1)), np.hstack((img2,img3)) ))

    # Show the frame (OpenCV assumes BRG color representation)
    cv2.imshow("Original image, BGR2RGB image, copied image and modified image", img_grid)
    
    # The waitKey command is needed to force openCV to show the image
    # It looks for a keystroke for x ms (with x the argument) and otherwise continues
    # In this case, the program halts until the user presses 'q'
    while True:
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