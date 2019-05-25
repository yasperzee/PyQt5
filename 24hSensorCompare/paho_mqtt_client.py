#!/usr/bin/ python
# ********************* python3 paho_mqtt_client.py ****************************
#
#   Description:    Subscribe selected sensors to mqtt run_local_server
#                   and send values to Google sheet.
#
#   Sensors:    BMP-180 / BMP-280 (temperature, pressure)
#               BME-280 (temperature, pressure, humidity)
#               DTH-11 / DTH22 (temperature,humidity)

#   paho-mqtt:
#   To obtain the full code, including examples and tests,
#   you can clone the git repository:
#        git clone https://github.com/eclipse/paho.mqtt.python
#*******************************************************************************
#TODO:  Add failsafe incase server not available
#TODO:  Get rid of globals
#TODO:  Clean up 'on_message' method ->  move sensor handling somewhere

"""-------- Version history ----------------------------------------------------
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
""""""--------------------------------------------------------------------------"""
from __future__ import print_function
import time

# Install paho-mqtt for python3 with pip3
import paho.mqtt.client as mqtt

from configuration import *
from GoogleSheetsHandler import Gredentials
from GoogleSheetsHandler import WriteNodeDataToSheet

class DataToSheet(WriteNodeDataToSheet):
    pass

# GLOBALS
semaf       = False
updateSheet = DataToSheet()

#*******************************************************************************
# The callback for when the client receives a CONNACK response from the mqtt-server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    for subst in subscription:
        client.subscribe(subst)

#*******************************************************************************
#*******************************************************************************
# The callback for when a PUBLISH message is received from the mqtt-server.
def on_message(client, userdata, msg):
    global semaf
    global updateSheets

    #print("on_message")
    #if (updateSheet.getUnsubscribe() == True):
    #    #print("unsubscribe")
    #    client.unsubscribe(subscription[-1])
    #    client.unsubscribe(subscription[-2])
    #    updateSheet.setUnsubscribe(False)

    semaf = True
    topic = (str(msg.topic))
    #print("topic is: " + topic)
    payload = (str(msg.payload))
    #print("payload is: " + payload)

    sensor = "Lampotila"
    if topic.endswith(sensor):
        updateSheet.setTemp(ERROR_VALUE)
        #print(sensor)
        payload = (str(msg.payload))
        tmp = (payload.split(': '))
        tmp = tmp.pop(1)
        tmp = (tmp.strip('}\''))
        temp = tmp.replace(".", ",")
        updateSheet.setTemp(temp)
        #testing = updateSheet.getTemp()
        #print("Temperature is: " + str(testing))

    sensor = "Ilmanpaine"
    if topic.endswith(sensor):
        updateSheet.setBaro(ERROR_VALUE)
        #print(sensor)
        payload = (str(msg.payload))
        tmp = (payload.split(': '))
        tmp = tmp.pop(1)
        tmp = (tmp.strip('}\''))
        baro = tmp.replace(".", ",")
        updateSheet.setBaro(baro)
        #testing = updateSheet.getBaro()
        #print("Barometer is: " + str(testing))

    sensor = "Korkeus";
    if topic.endswith(sensor):
        updateSheet.setAlti(ERROR_VALUE)
        #print(sensor)
        payload = (str(msg.payload))
        tmp = (payload.split(': '))
        tmp = tmp.pop(1)
        tmp = (tmp.strip('}\''))
        alti = tmp.replace(".", ",")
        updateSheet.setAlti(alti)
        #testing = updateSheet.getAlti()
        #print("Altitude is:" + str(testing))

    sensor = "Ilmankosteus";
    if topic.endswith(sensor):
        updateSheet.setHumid(ERROR_VALUE)
        #print(sensor)
        payload = (str(msg.payload))
        tmp = (payload.split(':'))
        tmp = tmp.pop(1)
        tmp = (tmp.strip('}\''))
        humid = tmp.replace(".", ",")
        updateSheet.setHumid(humid)
        #testing = updateSheet.getHumid()
        #print("Humidity is: " + str(testing))

    sensor = "Valoisuus";
    if topic.endswith(sensor):
        updateSheet.setALS(ERROR_VALUE)
        #print(sensor)
        payload = (str(msg.payload))
        tmp = (payload.split(':'))
        tmp = tmp.pop(1)
        tmp = (tmp.strip('}\''))
        als = tmp.replace(".", ",")
        updateSheet.setALS(als)
        #testing = updateSheet.getALS()
        #print("AmbientLight  is: " + str(testing))

    sensor = "Vcc";
    if topic.endswith(sensor):
        updateSheet.setVccBatt(ERROR_VALUE)
        #print(sensor)
        payload = (str(msg.payload))
        tmp = (payload.split(':'))
        tmp = tmp.pop(1)
        tmp = (tmp.strip('}\''))
        vcc = tmp.replace(".", ",")
        updateSheet.setVccBatt(vcc)
        #testing = updateSheet.getVccBatt()
        #print("Vcc  is: " + str(testing))

    sensor = "NodeInfo"
    if topic.endswith(sensor):
        #print(sensor)
        payload = (str(msg.payload))
        tmp = (payload.split(': '))
        tmp = tmp.pop(1)
        node_info = tmp.strip('}\'')
        tmp = (node_info.split('/'))
        nodemcu = tmp.pop(0)
        updateSheet.setNodeMcu(nodemcu)
        #testing = updateSheet.getNodeMcu()
        #print("Nodemcu is:      " + testing)
        sens = tmp.pop(0)
        updateSheet.setSensor(sens)
        #testing = updateSheet.getSensor()
        #print("Sensor is:      " + testing)
        node = tmp.pop(0)
        updateSheet.setNodeID(node)
        print("")
        testing = updateSheet.getNodeID()
        #print("NodeID is:" + testing)
        failcount = tmp.pop(0)
        updateSheet.setFailCount(failcount)
        #testing = updateSheet.getFailCount()
        #print("FailCount is:   " + testing)
        vcc = tmp.pop(0)
        updateSheet.setVccBatt(vcc)
        #testing = updateSheet.getVccBatt()
        #print("Vcc is:   " + testing)

    sensor = "TopicInfo"
    if topic.endswith(sensor):
        #print(sensor)
        payload = (str(msg.payload))
        tmp = (payload.split(':'))
        tmp = tmp.pop(1)
        location = tmp.strip('}\'')
        updateSheet.setLocation(str(location))
        #testing = updateSheet.getLocation()
        #print("Location is:     " + testing)

#*******************************************************************************
#*******************************************************************************

def main():
    global semaf
    global updateSheet

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)

    try:
        mqtt_client.connect (mqtt_connect_to[0], mqtt_connect_to[1], mqtt_connect_to[2])
    except:
        print("ERROR: Cannot connect to mqtt server " + mqtt_connect_to[0])
        quit()

    # If token.pickle does not exists, create newone.
    istoken = Gredentials()
    try:
        istoken.getToken();
    except FileNotFoundError:
        print("ERROR: No such file or directory: credentials.json")
        quit()

    creds = istoken.creds
    del istoken

    mqtt_client.loop_start()
    mqtt_client.on_connect = on_connect # Some timeout here?
    mqtt_client.on_message = on_message

    while True:
        if semaf:
            updateSheet.writeSensorDataToSheet(creds);
            semaf = False
        """
        if semaf:
            try:
                updateSheet.writeSensorDataToSheet(creds);
            except:
                print("ERROR: cannot write to sheet ")
                quit()
            finally:
                semaf = False
                """
    # def main()

main()
