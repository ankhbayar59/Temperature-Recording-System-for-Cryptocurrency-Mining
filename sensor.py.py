
import time
import datetime
import board
import busio
import adafruit_mcp9808
import jwt
import paho.mqtt.client as mqtt

"""
ssl_private_key_filepath =
ssl_algorithm = 
root_cert_filepath = 
project_id = 
google_cloud_platform_location = 
registry_id = 
device_id = 
"""

current_time = datetime.datetime.utcnow()
def create_jwt():
  token = {
      'iat': current_timee,
      'exp': current_time + datetime.timedelta(minutes=60),
      'aud': project_id
  }

  with open(ssl_private_key_filepath, 'r') as f:
    private_key = f.read()

  return jwt.encode(token, private_key, ssl_algorithm)

_CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, google_cloud_platform_location, registry_id, device_id)
_MQTT_TOPIC = '/devices/{}/events'.format(device_id)

client = mqtt.Client(client_id=_CLIENT_ID)

client.username_pw_set(
    username='unused',
    password=create_jwt())

def connect_error(err_c):
    return '{}: {}'.format(err_c, mqtt.error_string(err_c))

def connect(unusued_client, unused_userdata, unused_flags, err_c):
    print('connect', connect_errorr(err_c))

def publish(unused_client, unused_userdata, unused_mid):
    print('publish')



i2c_bus = busio.I2C(board.SCL, board.SDA)
temp_sensor = adafruit_mcp9808.MCP9808(i2c_bus)

client.on_connect = connect
client.on_publish = publish

client.tls_set(ca_certs=root_cert_filepath) 
client.connect('mqtt.googleapis.com', 8883)
client.loop_start()

# Could set this granularity to whatever we want based on device, monitoring needs, etc
temp_in_F = 0;

while True:
    temp_in_F = temp_sensor.temperature * 9 / 5 + 32
    #print('Temperature:', temp_in_F)
    payload = "Temperature: {temp}".format(temp = temp_in_F)
    client.publish(_MQTT_TOPIC, payload, qos=1)
    time.sleep(60)

client.loop_stop()
