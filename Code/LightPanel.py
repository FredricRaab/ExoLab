import board
import neopixel
import datetime  # Import the datetime module to work with dates and times
from datetime import time

class LightPanel:
    
    LEFT_PANEL = 1
    RIGHT_PANEL = 0

    RED = 0
    GREEN = 1
    BLUE = 2
    MAGENTA = 3
    WHITE = 4

    
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D21, 64, bpp=4) # Raspberry Pi wiring w 30 pixels
        self.leftLit = False
        self.rightLit = False
        self.leftBrightness = 0
        self.rightBrightness = 0
        self.leftOn = None
        self.leftOff = None
        self.rightOn = None
        self.rightOff = None

    def setTimeOn(self,side,HMstr):
        print("setTimeOn: ", side, HMstr)
        if (side == self.LEFT_PANEL):
            self.leftOn = HMstr
        else:
            self.rightOn = HMstr
            
    def setTimeOff(self,side,HMstr):
        print("setTimeOff: ", side, HMstr)
        if (side == self.LEFT_PANEL):
            self.leftOff = HMstr
        else:
            self.rightOff = HMstr   
  
    def setup(self, side, color, intensity):  
        if (side == self.LEFT_PANEL):
            self.leftColor = color
            self.leftIntensity = intensity
        else:
            self.rightColor = color
            self.rightIntensity = intensity
            
    def getSettingsStr(self):
        return str(self.leftOn) + "," + str(self.leftOff) + "," + \
               str(self.leftColor) + "," + str(self.leftBrightness) + "," + \
               str(self.rightOn) + "," + str(self.rightOff) + "," + \
               str(self.rightColor) + "," + str(self.rightBrightness)                              

# turn all off
    def all_off(self):
        self.pixels.fill((0,0,0,0))
        self.pixels.show
        self.leftBrightness = 0
        self.rightBrightness = 0
        self.leftLit = False
        self.rightLit = False
        
# turn all white for photo
    def all_white(self):
        self.pixels.fill((255,255,255,255))
        self.pixels.show

        
# restore to current state before call to all_white when taking photo at night
    def restore_state(self):
        if (self.leftLit):
            self.side_on(self.LEFT_PANEL, self.leftColor, self.leftIntensity)
        else:
            self.side_on(self.LEFT_PANEL, self.leftColor, 0)  # turn off after taking picture
            
        if (self.rightLit):
            self.side_on(self.RIGHT_PANEL, self.rightColor, self.rightIntensity)
        else:
            self.side_on(self.RIGHT_PANEL, self.rightColor, 0)  # turn off after taking picture
            
# turn all on
    def all_on(self):
        self.side_on(self.LEFT_PANEL, self.leftColor, self.leftIntensity)
        self.side_on(self.RIGHT_PANEL, self.rightColor, self.rightIntensity)
        self.leftBrightness = self.leftIntensity
        self.rightBrightness = self.rightIntensity
        self.leftLit = True
        self.RightLit = True
        
# turns one side on    
    def side_on(self, side, color, intensity):
        if (side == self.LEFT_PANEL):
            lower = 0   
            higher = 32
        else:
            lower = 32		# default RIGHT
            higher = 64
    
        value = (255 * intensity) /100
    
        for index in range(lower, higher):
            if color == self.RED:
                    self.pixels[index] = (value, 0, 0, 0)
            elif color == self.GREEN:
                    self.pixels[index] = (0, value, 0, 0)
            elif color == self.BLUE:
                    self.pixels[index] = (0, 0, value, 0)
            elif color == self.MAGENTA:
                    self.pixels[index] = (value, 0, value, 0)
            else:
                    self.pixels[index] = (value, value, value, value)  # default WHITE
         
        self.pixels.show
        
    def checkClock(self):
    
        lightChange = False
        now = datetime.datetime.now()
        current_time = time(now.hour, now.minute, now.second)
        if not self.leftLit:     # panel is off - check if time to turn on
            if ((current_time <= self.leftOff) and (current_time >= self.leftOn)):
                print("Turning left panel on @ ", current_time)
                self.side_on(self.LEFT_PANEL, self.leftColor, self.leftIntensity)
                self.leftBrightness = self.leftIntensity
                self.leftLit = True
                lightChange = True
        else:
            if ((current_time >= self.leftOn) and (current_time >= self.leftOff)):
                print("Turning left panel off @ ", current_time)
                self.side_on(self.LEFT_PANEL, self.leftColor, 0)
                self.leftBrightness = 0
                self.leftLit = False
                lightChange = True
                
        if not self.rightLit:     # panel is off - check if time to turn on
            if ((current_time <= self.rightOff) and (current_time >= self.rightOn)):
                print("Turning right panel on @ ", current_time)
                self.side_on(self.RIGHT_PANEL, self.rightColor, self.rightIntensity)
                self.rightBrightness = self.rightIntensity
                self.rightLit = True
                lightChange = True
        else:
            if ((current_time >= self.rightOn) and (current_time >= self.rightOff)):
                print("Turning right panel off @ ", current_time)
                self.side_on(self.RIGHT_PANEL, self.rightColor, 0)
                self.rightBrightness = 0
                self.rightLit = False
                lightChange = True
        return(lightChange)
    
