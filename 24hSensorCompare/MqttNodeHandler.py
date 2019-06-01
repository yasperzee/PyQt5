#!/usr/bin/ python
# ********************* MqttNodeHandler.py ****************************
#
#   Description:    Subscribe selected sensors to mqtt run_local_server
#                   and send values to Google sheet.
#
#   Sensors:    BMP-180 / BMP-280 (temperature, pressure)
#               BME-280 (temperature, pressure, humidity)
#               DTH-11 / DTH22 (temperature,humidity)
#               TEMT6000 (AmbientLight)

#   paho-mqtt:
#   To obtain the full code, including examples and tests,
#   you can clone the git repository:
#        git clone https://github.com/eclipse/paho.mqtt.python
#*******************************************************************************
#TODO:  Add failsafe incase server not available
#TODO:  Get rid of globals
#TODO:  Clean up 'on_message' method ->  move sensor handling somewhere

"""-------- Version history ----------------------------------------------------
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

#TODD: Prepare project stucture for Docker
""""""--------------------------------------------------------------------------"""
from __future__ import print_function
import time

from GoogleSheetsHandler import WriteNodeDataToSheet
from configuration import subscription

#class DataToSheet(WriteNodeDataToSheet):
#    pass
#updateSheet = DataToSheet()
updateSheet = WriteNodeDataToSheet()

#*******************************************************************************
class ReadMqttData:
    def __init__(self):
        self.topic      = "Empty"
        self.payload    = "Empty"
        self.semaf      =  False

    def __del__(self):
        class_name = self.__class__.__name__

    def set_data(self):
        topic = self.getTopic()
        payload = self.getPayload()

        #print("set_data")
        #print("set_data, topic is  :" + topic )
        #print("set_data, payload is:" + payload )

        nodefeat = "Lampotila"
        if topic.endswith(nodefeat):
            #print("nodefeat: " + nodefeat)
            tmp = (str(payload))
            tmp = (tmp.split(': '))
            tmp = tmp.pop(1)
            tmp = tmp.strip('}\'')
            updateSheet.setTemp(tmp)
            #print("Temperature is:" + updateSheet.getTemp())

        nodefeat = "Ilmanpaine"
        if topic.endswith(nodefeat):
            #print("nodefeat: " + nodefeat)
            tmp = (str(payload))
            tmp = (tmp.split(':'))
            tmp = tmp.pop(1)
            tmp = tmp.strip('}\'')
            updateSheet.setBaro(tmp)
            #print("Barometer is:" + updateSheet.getBaro())

        nodefeat = "Korkeus"
        if topic.endswith(nodefeat):
            #print("nodefeat: " + nodefeat)
            tmp = (str(payload))
            tmp = (tmp.split(':'))
            tmp = tmp.pop(1)
            tmp = tmp.strip('}\'')
            updateSheet.setAlti(tmp)
            #print("Altitude is:" + updateSheet.getAlti())

        nodefeat = "Ilmankosteus"
        if topic.endswith(nodefeat):
            #print("nodefeat: " + nodefeat)
            tmp = (str(payload))
            tmp = (tmp.split(':'))
            tmp = tmp.pop(1)
            tmp = tmp.strip('}\'')
            updateSheet.setHumid(tmp)
            #print("Humidity is:" + updateSheet.getHumid())

        nodefeat = "Valoisuus"
        if topic.endswith(nodefeat):
            print("nodefeat: " + nodefeat)
            tmp = (str(payload))
            tmp = (tmp.split(':'))
            tmp = tmp.pop(1)
            tmp = tmp.strip('}\'')
            updateSheet.setALS(tmp)
            #print("AmbientLight  is:" + updateSheet.getALS())

        nodefeat = "Vcc"
        if topic.endswith(nodefeat):
            #print("nodefeat: " + nodefeat)
            tmp = (str(payload))
            tmp = (tmp.split(': '))
            tmp = tmp.pop(1)
            tmp = tmp.strip('}\'')
            #print("Vcc is :" + updateSheet.getVcc())

        nodefeat = "NodeInfo"
        if topic.endswith(nodefeat):
            #print("nodefeat: " + nodefeat)
            payload = (str(payload))
            tmp = (payload.split(': '))
            tmp = tmp.pop(1)
            node_info = tmp.strip('}\'')
            tmp = (node_info.split('/'))
            nodemcu = tmp.pop(0)
            updateSheet.setNodeMcu(nodemcu)
            #print("Nodemcu is:" + updateSheet.getNodeMcu())
            sens = tmp.pop(0)
            updateSheet.setSensor(sens)
            #print("Sensor is:" + updateSheet.getSensor())
            node = tmp.pop(0)
            updateSheet.setNodeID(node)
            #print("NodeID is:" + updateSheet.getNodeID())
            failcount = tmp.pop(0)
            updateSheet.setFailCount(failcount)
            #print("FailCount is:" + updateSheet.getFailCount())

        nodefeat = "TopicInfo"
        if topic.endswith(nodefeat):
            #print("nodefeat: " + nodefeat)
            tmp = (str(payload))
            tmp = (tmp.split(': '))
            tmp = tmp.pop(1)
            tmp = tmp.strip('}\'')
            updateSheet.setLocation(tmp)
            #print("Location is:" + updateSheet.getLocation())

    # getters and setters
    def getSemaf(self):
        return self.semaf
    def setSemaf(self, semaf):
        self.semaf = semaf

    def getPayload(self):
        return self.payload
    def setPayload(self, payload):
        self.payload = payload

    def getTopic(self):
        return self.topic
    def setTopic(self, topic):
        self.topic = topic

#*******************************************************************************
# The callback for when the client receives a CONNACK response from the mqtt-server.
def on_connect(client, userdata, flags, rc):
    print("mqtt server connected.")
    #print("mqtt_server connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for subsc in subscription:
        client.subscribe(subsc)

#*******************************************************************************
# The callback for when a PUBLISH message is received from the mqtt-server.
def on_message(client, userdata, msg):
    mqtt_data_handler.setTopic(str(msg.topic))
    mqtt_data_handler.setPayload(str(msg.payload))
    #print("on_message, topic is  :" + mqtt_data_handler.getTopic())
    #print("on_message, payload is:" + mqtt_data_handler.getPayload())

    mqtt_data_handler.set_data()
    mqtt_data_handler.setSemaf(True)
