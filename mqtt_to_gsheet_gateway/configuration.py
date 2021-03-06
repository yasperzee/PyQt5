#!/usr/bin/ python3

# ********************* configuratrion.py **************************************
#
#   Description:        Configuraions for mqtt to google-sheet gateway
#
#   Dependencies:       Install with pip3:  paho-mqtt, google-api-python-client, google-auth-oauthlib

"""-------- Version history ----------------------------------------------------

    v1.9    yasperzee   6'19    No error count to sheet, sheet header re-arranged,
                                Format datetime together --> Release v1.0 -> combability brake to older versions!!!
    v1.8    yasperzee   6'19    Exception handling added for SHEET_NAME and MQTT_CLIENT_ID
    v1.7    yasperzee   6'19    mqtt host address secured
    v1.6    yasperzee   6'19    Prepare project stucture for Docker
    v1.5    yasperzee   6'19    mqtt_params is now dict
    v1.4    yasperzee   5'19    Cleaning for Release
    v1.3    yasperzee   5'19    ALS support (TEMT6000)
    v1.2.2  yasperzee   5'19    Sheet header updated
    v1.2.1  yasperzee   5'19    Branch to compare sensors 24h cycle
    v1.2    yasperzee   5'19    Use append to decrease trafic to sheet
    v1.1    yasperzee   4'19    Added error count to sheet
    v1.0    yasperzee   4'19    Added 3. sensor to Compare Sensors
    v0.9    yasperzee   4'19    Compare Sensors
    v0.8    yasperzee   4'19    Subscribtion definitions moved to configuration.py
    v0.7    yasperzee   4'19    MQTT_CLIENT_ID moved to configuration.py
    v0.6    yasperzee   4'19    Error handling if netrwork or mqtt_server not available
    v0.5    yasperzee   4'19    Read SENSOR and NODEMCU from node for SHEET_NAME
    v0.4    yasperzee   4'19    Read TOPIC from node, write altitude to sheet if publish by node.
    v0.3    yasperzee   4'19    Reads NodeInfo & Protocol from node
    v0.2    yasperzee   4'19    Edited for paho_mqtt_client.py
    v0.1    yasperzee   4'19    Configurations for weather_esp01_dht_http.py
                                Classes moved to separate modules

#TODO:
-----------------------------------------------------------------------------"""

""" Select some Topics to subscribe or add your ownones
"$SYS/#"
"Demo/#"
"Demo/Movable/#"
"Koti/#"
"Koti/Liikkuva/#"
"Koti/Olohuone/#"
"Koti/Olohuone/Lampotila"
"Koti/Olohuone/Ilmankosteus"
"Koti/Olohuone/Ilmanpaine"
"Koti/Olohuone/Korkeus"
"Koti/Olohuone/Valoisuus"
"Koti/Olohuone/NodeInfo"  # To find correct sheet on spreadsheet
"Koti/Olohuone/TopicInfo" # Location of the node
"""

#SUBS = "SLEEP_TESTING"
SUBS = "SUBSALL"

if SUBS == "SLEEP_TESTING":
    subscription = (
        "Koti/Testing/TopicInfo",       # NODE-00 / BMP280
        "Koti/Testing/NodeInfo",
        "Koti/Testing/Lampotila",
        "Koti/Testing/Ilmanpaine",
        "Koti/Testing/Korkeus",
        "Koti/Testing/Vcc"
        )
else:
    subscription = (
        "Koti/MH-1/NodeInfo",       # NODE-01 / DHT22 (ESP01)
        "Koti/MH-1/TopicInfo",
        "Koti/MH-1/Lampotila",
        "Koti/MH-1/Ilmankosteus",
        "Koti/Partsi/NodeInfo",     # NODE-02 / BMP180 (ESP01)
        "Koti/Partsi/TopicInfo",
        "Koti/Partsi/Lampotila",
        "Koti/Partsi/Ilmanpaine",
        "Koti/Partsi/Korkeus",
        "Koti/Olohuone/NodeInfo",   # NODE-04 / BMP280 & TEMT6000 (ESP12E)
        "Koti/Olohuone/TopicInfo",
        "Koti/Olohuone/Lampotila",
        "Koti/Olohuone/Ilmanpaine",
        "Koti/Olohuone/Korkeus",
        "Koti/Olohuone/Valoisuus"
        )

# Sheet named 'SHEET_NAME' must exist on Spreadsheet
SHEET_NAME = "CompareData"
#SHEET_NAME = "SleepTest"
#SHEET_NAME = "SensorData"
#SHEET_NAME = "UNSUPPORTED"

#MQTT_CLIENT_ID = "MqttClient_W530"
MQTT_CLIENT_ID = "MqttClient_RPI3"
#MQTT_CLIENT_ID = "MqttClient_N510"
#MQTT_CLIENT_ID = "SleepTest_"
#MQTT_CLIENT_ID = "Docker 01"

## First row to write data ( Header is 4 rows )
MIN_ROW = 5
# Make sure there is at least MAX_ROW+1 rows in sheet!
#MAX_ROW = 96 + MIN_ROW # 15min update interval => 96 records / 24h
MAX_ROW = 288 + MIN_ROW # 5min update interval => 288 records / 24h

#MAX_ROW = 672 + MIN_ROW # 15min update interval => 672 records / week(7days)
#MAX_ROW = 2688 + MIN_ROW # 15min update interval => 2688 records / month(4wk)
#MAX_ROW = 32256 + MIN_ROW # 15min update interval => 32256 records / year(12months)
         # 5 SENSORS --> 4*(7+4)+(5*(7+4)*32256) columns = 967 680 cells / year

# Range on sheet to write value, node info & topic(location)
value_range1      = '!A'+ str(MIN_ROW)
node_info_range1  = '!A2'
node_topic_range1 = '!A3'
value_range2      = '!E'+ str(MIN_ROW)
node_info_range2  = '!E2'
node_topic_range2 = '!E3'
value_range3      = '!J'+ str(MIN_ROW)
node_info_range3  = '!J2'
node_topic_range3 = '!J3'
value_range4      = '!O'+ str(MIN_ROW)
node_info_range4  = '!O2'
node_topic_range4 = '!O3'
value_range5      = '!Y'+ str(MIN_ROW)
node_info_range5  = '!Y2'
node_topic_range5 = '!Y3'

#Select port
#TCP/IP port 1883 is reserved with IANA for use with MQTT.
#TCP/IP port 8883 is also registered, for using MQTT over SSL.
MQTT_PORT = 1883
#MQTT_PORT = 8883
MQTT_KEEPALIVE = 60 # Seconds 0..120
MQTT_RECONN_DELAY = 30 # Seconds 0..120

# The ID of a spreadsheet.
SPREADSHEET_ID = '1bZ0gfiIlpTnHn-vMSA-m9OzVQEtF1l7ELNo40k0EBcM'
#SPREADSHEET_ID = '1bZ0gfiIlpTnHn-vMSA-m9OzVQEtF1l7ELNo40k0EBcMERRpr'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

try:
    SHEET_NAME
except NameError:
    SHEET_NAME = "ERROR"
if SHEET_NAME == "CompareData":
    SHEET_ID = 0 # CompareData
elif SHEET_NAME == "SleepTest":
    SHEET_ID = 1529352488 # SleepTest
elif SHEET_NAME == "SensorData":
    SHEET_ID = 2099931552 #SensorData
else:
    print('ERROR: unsupported SHEET_NAME or SHEET_NAME not defined')
    quit()

try:
    MQTT_CLIENT_ID
except NameError:
    print('ERROR: MQTT_CLIENT_ID not defined')
    quit()


ERROR_VALUE = -999,9
START_ROW_INDEX = MIN_ROW-1
END_ROW_INDEX = MAX_ROW
