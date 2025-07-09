import boto3
from botocore.exceptions import NoCredentialsError

class AWS:
    
    def __init__(self):
        self.bucket = "exolabdev"
        self.deviceSerialNumber ="Z100100"
        self.baseURL = "https://exolabdev.s3.us-west-1.amazonaws.com/"
        
    def setBucket(self, bucket):
        self.bucket = bucket
        
    def setDeviceSerialNumber(self, sn):
        self.deviceSerialNumber = sn
    
    def setBaseURL(self, url):
        self.baseURL = url
        
    def uploadToAWS(self, local_file, aws_file):
        s3 = boto3.client("s3")
        s3_file = self.deviceSerialNumber + "/" + aws_file
        
        try:
            s3.upload_file(local_file, self.bucket, s3_file)
            print ("Upload successful: " + s3_file)
            return self.baseURL + s3_file
        except FileNotFoundError:
            print("File not found" + local_file)
            return ""
        except NoCredentialsError:
            print ("No AWS credentials")
            return ""
        except Exception as e:
            print ("Unexpected Exception: " + str(e))
            return ""
