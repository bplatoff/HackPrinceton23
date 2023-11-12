import random
import time
import cv2
import base64

from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=CropManagementSystem.azure-devices.net;DeviceId=RaspberryPI;SharedAccessKey=d5zKts5ijw3nmwXvElrCS/7589NKi0Y7CAIoTJm7AYU="

TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}, "image":{image}}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        while True:
            # Build the message with simulated telemetry values.
            temperature = TEMPERATURE + (random.random() * 15)
            humidity = HUMIDITY + (random.random() * 20)

            image = cv2.VideoCapture(0)
            ret, frame = image.read()
            image.release()

            resized_image = cv2.resize(frame, (224, 224))
            image = cv2.imencode(".jpg", resized_image)[1]
            image = base64.b64encode(image).decode("utf-8")

            msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity, image=image)
            message = Message(msg_txt_formatted)
            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            if temperature > 30:
              message.custom_properties["temperatureAlert"] = "true"
            else:
              message.custom_properties["temperatureAlert"] = "false"
            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(3)
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()