#!/usr/bin/ python3

"""------------------------------ Version history ------------------------------
    v1.3    yasperzee   5'19    Remove DHT11 and DHT22 support
    v1.2.3  yasperzee   5'19    SleepTest
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


-----------------------------------------------------------------------------"""
# ToDo: support for AmbientLightSensor
# Supported sensors
# BMP180, BMP280, BME280
# Verified sensors
# BMP180

""" Select some Topics from here or add your ownones
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
"Koti/Parveke/Valoisuus",
"Koti/Olohuone/NodeInfo"  # To find correct sheet on spreadsheet
"Koti/Olohuone/TopicInfo" # For location of node
"""
# Sheet named 'SHEET_NAME' must exist on Spreadsheet
SHEET_NAME   = "SleepTest"
SHEET_ID = 1529352488 # SleepTest

#SHEET_NAME   = "CompareData"
#SHEET_ID = 0 # CompareData

#SHEET_NAME   = "SensorData"
#SHEET_ID = 2099931552 #SensorData

subscription = ("Koti/Parveke/Lampotila",   # NODE-03 / BMP180
                "Koti/Parveke/Ilmanpaine",
                "Koti/Parveke/Korkeus",
                "Koti/Parveke/NodeInfo",
                "Koti/Parveke/TopicInfo"
                )

# Select mqtt server connect to
#mqtt_connect_to = ("xxx.xxx.xxx,xxx", 1883, 60) # Phone, DEMO / RPI3
#mqtt_connect_to = ("192.168.10.52", 1883, 60) # Local RPI3
#mqtt_connect_to = ("192.168.10.34", 1883, 60) # Local W530
mqtt_connect_to = ("192.168.10.63", 1883, 60) # Local NP-510

MQTT_CLIENT_ID = "MqttClient_W530"
#MQTT_CLIENT_ID = "MqttClient_RPI3"
#MQTT_CLIENT_ID = "MqttClient_N510"

# The ID of a spreadsheet.
SPREADSHEET_ID  = '1bZ0gfiIlpTnHn-vMSA-m9OzVQEtF1l7ELNo40k0EBcM'
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

MIN_ROW     = 5
# Make sure there is at least MAX_ROW+1 rows in sheet!
#MAX_ROW     = 96 + MIN_ROW # 15min update interval => 96 records / day(24h)
#MAX_ROW     = 288+ MIN_ROW # 15min update interval => 288 records / 72h
MAX_ROW     = 672+ MIN_ROW # 15min update interval => 672 records / week(7days)
#MAX_ROW     = 2688+ MIN_ROW # 15min update interval => 2688 records / month(4wk)
#MAX_ROW     = 32256+ MIN_ROW # 15min update interval => 32256 records / year(12months)

# Shells on sheet to write node info, topic & altitude
node_info_range3     = '!A2'
node_topic_range3    = '!A3'

# Sheet named 'SHEET_NAME' must exist on Spreadsheet
value_range3 = SHEET_NAME + '!A'+ str(MIN_ROW)

ERROR_VALUE = -999,9
