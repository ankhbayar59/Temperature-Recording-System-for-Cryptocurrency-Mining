from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient 
import Adafruit_DHT
import time

ENDPOINT = "a1nfu30dqjq7nl-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "sensor client"
PATH_TO_CERT = "/home/pi/6338ebc78a-certificate.pem.crt"
PATH_TO_KEY = "/home/pi/6338ebc78a-private.pem.key"
PATH_TO_ROOT = "/home/pi/root.pem"

sensor_MQTT_Client = AWSIoTMQTTClient(CLIENT_ID)
sensor_MQTT_Client.configureEndpoint(ENDPOINT, 8883)
sensor_MQTT_Client.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)
sensor_MQTT_Client.configureOfflinePublishQueueing(-1)  
sensor_MQTT_Client.configureDrainingFrequency(2)
sensor_MQTT_Client.configureConnectDisconnectTimeout(10)  
sensor_MQTT_Client.configureMQTTOperationTimeout(5) 

temperatureSensorName = Adafruit_DHT.DHT11




sensor_MQTT_Client.connect()
 
   
while 1: 
    humidity, temperature = Adafruit_DHT.read_retry(temperatureSensorName, 17)
    
    f_temperature = temperature * (1.8) + 32
    
    payload = str(f_temperature)

    print payload 
    
    #publishing the sensor's temperature data to AWS IOT thing named "sensorValue"
    
    sensor_MQTT_Client.publish("sensorValue", payload, 0) #publish the payload
    
    time.sleep(2)
