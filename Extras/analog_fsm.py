# This program demonstrates how to use the ADC


# General libraries
import time
# Libraries for the ADC
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


# Hardware SPI configuration:
# Connect the chip to the following pins
#     MCP3008           RPI
#       VDD       to      3.3V
#       VREF      to      3.3V
#       AGND      to      GND
#       CLK       to      GPIO 11 (physical pin 23; SPIO SCLK)
#       DOUT      to      GPIO 9  (physical pin 21; SPIO MISO)
#       DIN       to      GPIO 10 (physical pin 19; SPIO MOSI)
#       CS/SHDN   to      GPIO 8  (physical pin 24; SPIO CS0) 
#       DGND      to      GND
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.CE0)
mcp = MCP.MCP3008(spi, cs)

# Create analog input channels for all 8 channels
channels = [AnalogIn(mcp, getattr(MCP, 'P%d' % i)) for i in range(8)]

# Initialize the finite state machine
FSM1State = 0
FSM1NextState = 0
FSM1LastTime = 0


try:
    print("Press CTRL+C to end the program.")
    print("Reading values")
        
    while True:
       
        # Check the current time
        currentTime = time.time()

        # Update the state
        FSM1State = FSM1NextState
        
        # Check the state transitions for FSM 1
        if (FSM1State == 0):
            if (currentTime - FSM1LastTime > 0.5):
                values = [0]*8
                for i in range(8):
                    values[i] = channels[i].value
                print(' | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
                FSM1NextState = 1
            else:
                FSM1NextState = 0
                
        elif (FSM1State == 1):      # dummy state so that delay works
            FSM1NextState = 0 
              
        else:
            print("Error: unrecognized state for FSM1")
            break   

        # If there is a state change, record the time    
        if (FSM1State != FSM1NextState):
            FSM1LastTime = currentTime           


# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
    pass    
finally:
    # Clean up the resources
    pass
