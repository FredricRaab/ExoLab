import board
import busio
from time import sleep
import adafruit_character_lcd.character_lcd_i2c as character_lcd


class LCD:
    
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.lcd = None
        try:
            self.lcd = character_lcd.Character_LCD_I2C(self.i2c, 16, 2, 0x20)
            self.lcd.backlight = True
        except:
            print("No LCD display connected.")
        
    def message(self, message):
        if (self.lcd == None):
            print("LCD: " + message)
        else:    
            self.lcd.clear()
            self.lcd.message = message
        
    def scrollMessage(self, message):
        if (self.lcd == None):
            print("LCD Scroll: " + message)
        else:
            if len(message) <= 16:
                self.lcd.clear()
                self.lcd.message = message  # no need to scoll message
            else:
                for i in range(2):		# repeat 2x
                    self.lcd.clear()
                    self.lcd.message = message
                    sleep(3)
                for j in range(len(message)-16):
                    sleep(0.5)
                    self.lcd.move_left()
                
    def displayData(self, temp, humd, co2, lux):
        message = f"Temp:{temp} Humd:{humd}\nCO2:{co2} L:{lux}"
        self.message(message)
