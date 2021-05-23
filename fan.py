import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient 

import RPi.GPIO as GPIO



ENDPOINT = "a1nfu30dqjq7nl-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "fan client"
PATH_TO_CERT = "/home/pi/6338ebc78a-certificate.pem.crt"
PATH_TO_KEY = "/home/pi/6338ebc78a-private.pem.key"
PATH_TO_ROOT = "/home/pi/root.pem"

fan_MQTT_Client = AWSIoTMQTTClient(CLIENT_ID)
fan_MQTT_Client.configureEndpoint(ENDPOINT, 8883)
fan_MQTT_Client.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)
fan_MQTT_Client.configureOfflinePublishQueueing(-1)  
fan_MQTT_Client.configureDrainingFrequency(2)
fan_MQTT_Client.configureConnectDisconnectTimeout(10)  
fan_MQTT_Client.configureMQTTOperationTimeout(5) 

 
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)

GPIO.setup(27, GPIO.OUT)

 

pwmOut = GPIO.PWM(17, 200)

pwmOut.start(0)

fan_MQTT_Client.connect()


def payload(self, params, packet):
   global dutyCycle
   dutyCycle = 0
   temperature = int(float(packet.payload))
   if(temperature <= 60):
      dutyCycle = 40
      GPIO.output(27, GPIO.LOW)
      print(dutyCycle)
      print("temperature is : " + str(temperature) + "F")
   elif(temperature > 80):
      dutyCycle = 100
      GPIO.output(27, GPIO.HIGH)
      print(dutyCycle)
      print("temperature is : " + str(temperature) + "F")
   else:
      temp = temperature - 60
      dutyCycle = (temp * 3) + 40
      GPIO.output(27, GPIO.LOW)
      print(dutyCycle)
      print("temperature is : " + str(temperature) + "F")

fan_MQTT_Client.subscribe("sensorValue", 1, payload)

while(1):
   time.sleep(4)
   pwmOut.ChangeDutyCycle(100 - dutyCycle)
   
