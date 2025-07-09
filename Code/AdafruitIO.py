from Adafruit_IO import Client, Feed, Data, RequestError

class AdafruitIO:
    
    def __init__(self):
        self.userName = None
        self.userKey = None
        
    def setUserName(self, name):
        self.userName = name
        
    def setUserKey(self, key):
        self.userKey = key

# These feed labels depend on how you defined your dashboard
    def openFeeds(self):
        try:
            self.aio = Client(self.userName, self.userKey)
            self.temperature = self.aio.feeds('exolabgroupfeed.temperature')
            self.humidity = self.aio.feeds('exolabgroupfeed.humidity')
            self.CO2 = self.aio.feeds('exolabgroupfeed.co2')
            self.lux = self.aio.feeds('exolabgroupfeed.lux')
            self.leftColor = self.aio.feeds('exolabgroupfeed.left-color')
            self.leftIntensity = self.aio.feeds('exolabgroupfeed.left-intensity')
            self.rightColor = self.aio.feeds('exolabgroupfeed.right-color')
            self.rightIntensity = self.aio.feeds('exolabgroupfeed.right-intensity')
        except Exception as e:
            print("Can't open Adafruit feed: " + str(e))


    def sendData(self,temp,humd,co2,lux,lc,li,rc,ri):
        try:
            self.aio.send_data(self.temperature.key, temp)
            self.aio.send_data(self.humidity.key, humd)
            self.aio.send_data(self.CO2.key, co2)
            self.aio.send_data(self.lux.key, lux)
            self.aio.send_data(self.leftColor.key, lc)
            self.aio.send_data(self.leftIntensity.key, li)
            self.aio.send_data(self.rightColor.key, rc)
            self.aio.send_data(self.rightIntensity.key, ri)
        except Exception as e:
            print("Error sending data to AdafruitIO: " + str(e))

