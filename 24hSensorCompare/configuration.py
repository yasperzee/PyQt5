#!/usr/bin/ python3

"""------------------------------ Version history ------------------------------
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

#TODD:
-----------------------------------------------------------------------------"""

# Supported sensors
# DHT11, DHT22, BMP180, BMP280, BME280, TEMT6000
# Verified sensors
# DHT11, DHT22, BMP180, BMP280, TEMT6000

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
"Koti/Olohuone/TopicInfo" # For location of node
"""
# First row to write data
MIN_ROW = 5
# Make sure there is at least MAX_ROW+1 rows in sheet
#MAX_ROW     = 96 + MIN_ROW # 15min update interval => 96 records / 24h
MAX_ROW = 288 + MIN_ROW # 5min update interval => 288 records / 24h

START_ROW_INDEX = MIN_ROW-1
END_ROW_INDEX = MAX_ROW

# Sheet named 'SHEET_NAME' must exist on Spreadsheet
SHEET_NAME   = "CompareData"
#SHEET_NAME   = "SleepTest"
#SHEET_NAME   = "SensorData"

# Range on sheet to write value, node info & topic(location)
value_range1         = '!A'+ str(MIN_ROW)
node_info_range1     = '!A2'
node_topic_range1    = '!A3'

value_range2         = '!F'+ str(MIN_ROW)
node_info_range2     = '!F2'
node_topic_range2    = '!F3'

value_range3         = '!K'+ str(MIN_ROW)
node_info_range3     = '!K2'
node_topic_range3    = '!K3'

value_range4         = '!R'+ str(MIN_ROW)
node_info_range4     = '!R2'
node_topic_range4    = '!R3'


subscription = ("Koti/Olohuone/Lampotila",  # NODE-01 / DHT11
                "Koti/Olohuone/Ilmankosteus",
                "Koti/Olohuone/NodeInfo",
                "Koti/Olohuone/TopicInfo",
                "Koti/Ulkoilma/Lampotila",  # NODE-02 / DHT22
                "Koti/Ulkoilma/Ilmankosteus",
                "Koti/Ulkoilma/NodeInfo",
                "Koti/Ulkoilma/TopicInfo",
                "Koti/Partsi/Lampotila",# NODE-03 / BMP180 & TEMT6000
                "Koti/Partsi/Ilmanpaine",
                "Koti/Partsi/Korkeus",
                "Koti/Partsi/Valoisuus",
                "Koti/Partsi/Vcc",
                "Koti/Partsi/NodeInfo",
                "Koti/Partsi/TopicInfo",
                "Koti/Parveke/Lampotila",# NODE-04 / BMP280
                "Koti/Parveke/Ilmanpaine",
                "Koti/Parveke/Korkeus",
                #"Koti/Parveke/Valoisuus",
                #"Koti/Parveke/Vcc",
                "Koti/Parveke/NodeInfo",
                "Koti/Parveke/TopicInfo"
                )

# Select mqtt server connect to
#mqtt_connect_to = ("192.168.10.50", 1883, 60) # Phone, DEMO / RPI3, Wlan
#mqtt_connect_to = ("192.168.10.52", 1883, 60) # Local RPI3, LAN
#mqtt_connect_to = ("192.168.10.34", 1883, 60) # Local W530
mqtt_connect_to = ("192.168.10.63", 1883, 60) # Local NP-510

#MQTT_CLIENT_ID = "MqttClient_W530"
#MQTT_CLIENT_ID = "MqttClient_RPI3"
MQTT_CLIENT_ID = "MqttClient_N510"

# The ID of a spreadsheet.
SPREADSHEET_ID  = '1bZ0gfiIlpTnHn-vMSA-m9OzVQEtF1l7ELNo40k0EBcM'
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

if SHEET_NAME== "CompareData":
    SHEET_ID = 0 # CompareData

elif SHEET_NAME== "SleepTest":
    SHEET_ID = 1529352488 # SleepTest

elif SHEET_NAME== "SensorData":
    SHEET_ID = 2099931552 #SensorData

else:
    print('Select SHEET!')
    # try:

ERROR_VALUE = -999,9
