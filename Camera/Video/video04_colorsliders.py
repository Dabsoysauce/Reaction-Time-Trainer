# This program illustrates how to capture frames in a video stream
# and how to do extract pixels of a specific color
# It includes a slider to adjust the color that is being filtered


# General libraries
import time
import numpy as np 
# Libraries to control the camera
from picamera2 import Picamera2
from libcamera import Transform
import cv2


# Create the track bars
cv2.namedWindow('trackbars')
cv2.moveWindow('trackbars',10,100)
def nothing(x):
    pass
cv2.createTrackbar('h lower','trackbars', 100, 180, nothing)
cv2.createTrackbar('s lower','trackbars', 0, 255, nothing)
cv2.createTrackbar('v lower','trackbars', 0, 255, nothing)
cv2.createTrackbar('h upper','trackbars', 175, 180, nothing)
cv2.createTrackbar('s upper','trackbars', 255, 255, nothing)
cv2.createTrackbar('v upper','trackbars', 255, 255, nothing)
img_low = np.zeros((15,512,3),np.uint8)
img_high = np.zeros((15,512,3),np.uint8)


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

        # Get the size of the np array
        w,h,d = img.shape
        
        #-----------------------------------------------------
        # We will use numpy to do all our image manipulations
        #-----------------------------------------------------

        # Convert for BGR to HSV color space, using OpenCV
        # The reason is that it is easier to extract colors in the HSV space
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Get info from the trackbars
        h1 =  cv2.getTrackbarPos('h lower','trackbars')
        s1 =  cv2.getTrackbarPos('s lower','trackbars')
        v1 =  cv2.getTrackbarPos('v lower','trackbars')
        h2 =  cv2.getTrackbarPos('h upper','trackbars')
        s2 =  cv2.getTrackbarPos('s upper','trackbars')
        v2 =  cv2.getTrackbarPos('v upper','trackbars')
        img_low[:] = [h1,s1,v1]
        img_high[:] = [h2,s2,v2]
           
        # Define the range colors to filter; these numbers represent HSV
        lowerColorThreshold = np.array([h1,s1,v1])
        upperColorThreshold = np.array([h2,s2,v2])

        # Threshold the HSV image to get only colors in a range
        # The colors in range are set to white (255), while the colors not in range are set to black (0
        mask = cv2.inRange(img_hsv, lowerColorThreshold, upperColorThreshold)

        # Bitwise AND of the mask and the original image
        img_masked = cv2.bitwise_and(img, img, mask = mask)


        # Prepare the mask to be displayed in the grid and create a black image
        # Combine the four images into one larger image in a 2x2 grid      
        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        blank = np.zeros((w,h,d), np.uint8)
        img_grid = np.vstack(( np.hstack((img,mask_bgr)), np.hstack((img_masked,blank)) ))

        # Show the frame (OpenCV assumes BRG color representation)
        cv2.imshow("Orginal frame, mask and masked frame", img_grid)

        # Alternatively, we could have shown the frames separately
        #cv2.imshow("Original frame", img)
        #cv2.imshow("Mask", mask)
        #cv2.imshow("Masked image", img_masked)

        # Display the trackbar window
        trackbars = np.vstack((cv2.cvtColor(img_low, cv2.COLOR_HSV2BGR),cv2.cvtColor(img_high, cv2.COLOR_HSV2BGR)))
        cv2.imshow('trackbars', trackbars)
        
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