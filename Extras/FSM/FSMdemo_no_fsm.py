# Illustration of a basic program (to compare it to the
# finite state machine implementation)
# Functionality: print information for the user


# General libraries
import time
 

try:
    print("Press CTRL+C to end the program.")
        
    while True:

        time.sleep(0.7)
        
        print (" ** Hello **")
     
        time.sleep(0.4)
        
        print (" ** How are you? **")

        time.sleep(1.0)
        
        print (" ** What's up? **")               


            
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:
    # Clean up the resources
    pass
