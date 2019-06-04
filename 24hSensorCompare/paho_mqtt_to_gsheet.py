#!/usr/bin/ python

# ***************** python3 paho_mqtt_client.py ********************************
#
#   Description:    Subscribe selected sensors to mqtt run_local_server
#                   and send values to Google sheet.
#
#   Sensors:        BMP-180 / BMP-280 (temperature, pressure)
#                   BME-280 (temperature, pressure, humidity)
#                   DTH-11 / DTH22 (temperature,humidity)
#                   TEMT6000 (AmbientLight)
#
#   paho-mqtt:      Install paho-mqtt for python3 with pip3
#   To obtain the full code, including examples and tests, you can clone the git repository:
#                   git clone https://github.com/eclipse/paho.mqtt.python
#
#*******************************************************************************

"""-------- Version history ----------------------------------------------------
    v1.5    yasperzee   6'19    mqtt_params is now dict
    v1.4    yasperzee   5'19    Separate mqtt_hanlder to separate module
    v1.3    yasperzee   5'19    Cleaning for Release
    v1.2    yasperzee   5'19    ALS support (TEMT6000)
    v1.1    yasperzee   5'19    vcc_batt
    v1.0    yasperzee   4'19    Prints fixed
    v0.9    yasperzee   4'19    Subscribtion definitions moved to configuration.py
    v0.8    yasperzee   4'19    Error handling if cannot write to sheet
    v0.7    yasperzee   4'19    Error handling if Gredentials cannot generate
                                MQTT_CLIENT_ID moved to configuration.py
    v0.6    yasperzee   4'19    Error handling if netrwork or mqtt_server not available
    v0.5    yasperzee   4'19    Read SENSOR and NODEMCU from node for SHEET_NAME
    v0.4    yasperzee   4'19    Reads topic_info from node
    v0.6    yasperzee   4'19    Reads NodeIn´fo from node, reads Altitude too
    v0.5    yasperzee   4'19    Synching with DHTxx version 1.1, Classes to separate modules
    v0.4    yasperzee   3'19    Change decimal separator to comma, sheets does not understand dot.
    v0.3    yasperzee   3'19    Add Google sheet handling
    v0.2    yasperzee   3'19    Subscribe "Koti/#"
    v0.1    yasperzee   3'19    Eclipse paho-mqtt client testing

#TODO:  Add failsafe incase server not available
#TODO:  Get rid of globals
#TODO:  Clean up 'on_message' method ->  move sensor handling somewhere
#TODO:

""""""-----------------------------------------------------------------------"""

from __future__ import print_function
import time

# Install paho-mqtt for python3 with pip3
import paho.mqtt.client as mqtt
from GoogleSheetsHandler import Gredentials
from GoogleSheetsHandler import WriteNodeDataToSheet
from MqttNodeHandler import updateSheet
#from MqttNodeHandler import mqtt_data_handler
from MqttNodeHandler import ReadMqttData
from MqttNodeHandler import on_connect
from MqttNodeHandler import on_message
from configuration import mqtt_params

mqtt_data_handler = ReadMqttData()

#*******************************************************************************
# The callback for when a PUBLISH message is received from the mqtt-server.
def on_message_old(client, userdata, msg):

    mqtt_data_handler.setTopic(str(msg.topic))
    mqtt_data_handler.setPayload(str(msg.payload))

    #print("on_message, topic is  :" + mqtt_data_handler.getTopic())
    #print("on_message, payload is:" + mqtt_data_handler.getPayload())

    mqtt_data_handler.set_data()
    #setData()
    mqtt_data_handler.setSemaf(True)

#*******************************************************************************
def main():

    print("HELLO FROM DOCKER!")

    # If token.pickle does not exists, create newone.
    istoken = Gredentials()
    try:
        istoken.getToken();
    except FileNotFoundError:
        print("ERROR: No such file or directory: credentials.json")
        quit()

    creds = istoken.creds
    del istoken

    mqtt_client = mqtt.Client(mqtt_params['mqtt_clien_id'])
    mqtt_client.loop_start()
    mqtt_client.on_connect = on_connect
    #mqtt_client.on_message = on_message
    mqtt_client.on_message = on_message_old

    try:
        mqtt_client.connect(mqtt_params['mqtt_host'],
                            mqtt_params['mqtt_port'],
                            mqtt_params['mqtt_keepalive']
                            )

    except:
        print("ERROR: Cannot connect to mqtt server " + MQTT_HOST)
        quit()

    while True:
        if mqtt_data_handler.getSemaf():
            #mqtt_client.disconnect
            print("MAIN: Entering writeSensorDataToSheet")
            updateSheet.writeSensorDataToSheet(creds);
            mqtt_data_handler.setSemaf(False)

        """
        if updateSheet.getSemaf():
            try:
                updateSheet.writeSensorDataToSheet(creds);
            except:
                print("ERROR: cannot write to sheet ")
                quit()
            finally:
                updateSheet.setSemaf(False)
                """
    # def main()

main()
mqtt_data_handler
