# This program illustrates how to capture frames in a video stream
# and how to do extract pixels of a specific color


# General libraries
import time
import numpy as np 
# Libraries to control the camera
from picamera2 import Picamera2
from libcamera import Transform
import cv2                                      


# Define the range colors to filter; these numbers represent HSV
lowerColorThreshold = np.array([0, 30, 60])
upperColorThreshold = np.array([20, 150, 255])


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
    transform = Transform(hflip = False, vflip = False)
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
        
        # Convert for BGR to HSV color space, using OpenCV
        # The reason is that it is easier to extract colors in the HSV space
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only colors in a range
        # The colors in range are set to white (255), while the colors not in range are set to black (0)
        mask = cv2.inRange(img_hsv, lowerColorThreshold, upperColorThreshold)

        # Count the number of white pixels in the mask
        numpixels = cv2.countNonZero(mask)
        print("Number of pixels in the color range:", numpixels)
       
        # Get the size of the array (the mask is of type 'numpy')
        # This should be 640 x 480 as defined earlier
        numx, numy = mask.shape

        # Select a part of the image and count the number of white pixels
        mask_center = mask[ numx//4 : 3*numx//4 , numy//4 : 3*numy//4 ]
        numpixels_center = cv2.countNonZero(mask_center)
        print("Number of pixels in the color range in the center part of the image:", numpixels_center)
           
        # Bitwise AND of the mask and the original image
        img_masked = cv2.bitwise_and(img, img, mask = mask)


        # Prepare the mask to be displayed in the grid
        # Combine the four images into one larger image in a 2x2 grid      
        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        img_grid = np.vstack(( np.hstack((img,mask_bgr)), np.hstack((img_masked,img_hsv)) ))

        # Show the frame (OpenCV assumes BRG color representation)
        cv2.imshow("Original frame, mask, masked frame and hsv frame", img_grid)
        
        # Alternatively, we could have shown the frames separately
        #cv2.imshow("Original frame", img)
        #cv2.imshow("Frame in HSV", img_hsv)
        #cv2.imshow("Mask", mask)
        #cv2.imshow("Masked image", img_masked) 
        
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
