#!/usr/bin/ python3

# ***************** GoogleSheetsHandlergle.py **********************************
#
#   Description:    Writes data received from mqtt server to the google sheet
#
#   Dependencies:   Install google-api-python-client for python3 with pip3
#                   Install google-auth-oauthlib for python3 with pip3
#
#*******************************************************************************
"""---------------------------- Version history --------------------------------

    v1.9    yasperzee   6'19    No error count to sheet, sheet header re-arranged,
                                Format datetime together --> Release v1.0 -> combability brake to older versions!!!

    v1.4    yasperzee   6'19    Exception handling added here and there to avoid
                                app crash on runtime if access to spreadsheet not available
    v1.4    yasperzee   5'19    Cleaning for Release
    v1.3    yasperzee   5'19    ALS support (TEMT6000)
    v1.2.2  yasperzee   5'19    Sheet header updated
    v1.2.1  yasperzee   5'19    Branch to compare sensors 24h cycle
                                GoogleSheetsApi Copy/Paste request method
    v1.2    yasperzee   5'19    Use append to decrease trafic with sheet
    v1.1    yasperzee   5'19    vcc_batt
    v1.0    yasperzee   4'19    Added error count to sheet
    v0.9    yasperzee   4'19    Added 3. sensor to Compare Sensors
    v0.8    yasperzee   4'19    Compare Sensors
    v0.7    yasperzee   4'19    prints fixed
    v0.6    yasperzee   4'19    Flag 'unsubscribe' added
    v0.5    yasperzee   4'19    Read SENSOR and NODEMCU from node for SHEET_NAME
    v0.4    yasperzee   4'19    Read altitude and topic-info from node.
    v0.3    yasperzee   4'19    Protocol info added to NodeInfo
    v0.2    yasperzee   4'19    Read NodeInfo & Protocol from node
    v0.1    yasperzee   4'19    Copied & modified for paho_mqtt_client.ph
    v0.1    yasperzee   4'19    Classes moved to separate modules
                                Classes to write sensor data to sheet for weather_esp01_dht_http.py

#TODD:
-----------------------------------------------------------------------------"""
import os.path
import pickle
#import datetime
import time
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from configuration import *

class WriteNodeDataToSheet:
    def __init__(self):
        self.datetime   = "Empty!"
        self.temp       = "N/A"
        self.humid      = "N/A"
        self.baro       = "N/A"
        self.alti       = "N/A"
        self.als        = "N/A"
        self.failCount  = "?"
        self.vcc        = "N/A"
        self.nodemcu    = "Unknown MCU!"
        self.sensor     = "Unknown SENSOR!"
        self.node_id    = "Unknown NODE!"
        self.location   = "Unknown LOCATION!"

    def __del__(self):
        class_name = self.__class__.__name__

    def readSheet(self, creds):
        pass

    def writeSensorDataToSheet(self, creds):
        self.creds = creds
        # Supported APIs w/ versions: https://developers.google.com/api-client-library/python/apis/
        # https://developers.google.com/sheets/api/
        # Build the service object
        try:
            service = build('sheets', 'v4', credentials=self.creds);
        except:
            print('build FAIL!')
            return

        try:
            spreadsheet = service.spreadsheets(); # Returns the spreadsheets Resource.
        except:
            print('service FAIL!')
            return

        # current date and time
        now = datetime.now()
        dt = now.strftime("%d/%m/%Y, %H:%M")
        self.datetime = str(dt)
        print("\n" + self.datetime)

        # check if node_id received from node is valid
        if self.node_id == "NODE-00": # Sleep Test
            value_range      = SHEET_NAME + value_range1
            node_topic_range = node_topic_range1
            node_info_range  = node_info_range1
            START_COLUMN_INDEX = 0  #A
            END_COLUMN_INDEX = 5    # date, time, temp, baro, Vcc
        elif self.node_id == "NODE-01":
            value_range      = SHEET_NAME + value_range1
            node_topic_range = node_topic_range1
            node_info_range  = node_info_range1
            START_COLUMN_INDEX = 0  #A
            END_COLUMN_INDEX = 3    # datetime, temp, humid
        elif self.node_id == "NODE-02":
            value_range      = SHEET_NAME + value_range2
            node_topic_range = node_topic_range2
            node_info_range  = node_info_range2
            START_COLUMN_INDEX = 4  #F
            END_COLUMN_INDEX = 7    # datetime, temp, humid
        elif self.node_id == "NODE-03":
            value_range      = SHEET_NAME + value_range3
            node_topic_range = node_topic_range3
            node_info_range  = node_info_range3
            START_COLUMN_INDEX = 10 #K
            END_COLUMN_INDEX = 13   # date, time, temp, ( baro, als to 1. row only)
        elif self.node_id == "NODE-04":
            value_range      = SHEET_NAME + value_range4
            node_topic_range = node_topic_range4
            node_info_range  = node_info_range4
            START_COLUMN_INDEX = 17 #R
            END_COLUMN_INDEX = 22   # date, time, temp, baro, als
        elif self.node_id == "NODE-05":
            value_range      = SHEET_NAME + value_range5
            node_topic_range = node_topic_range5
            node_info_range  = node_info_range5
            START_COLUMN_INDEX = 24 #Y
            END_COLUMN_INDEX = 29   # date, time, temp, baro, als
        else:
            print('Unsupported NODE-id!')
            return

        batch_update_spreadsheet_request_body = [
            {
            "copyPaste": {
                "source": {
                    "sheetId": SHEET_ID,
                    "startRowIndex": START_ROW_INDEX,
                    "endRowIndex": END_ROW_INDEX,
                    "startColumnIndex": START_COLUMN_INDEX,
                    "endColumnIndex": END_COLUMN_INDEX
                    },
                "destination": {
                    "sheetId": SHEET_ID,
                    "startRowIndex": MIN_ROW,
                    "endRowIndex": END_ROW_INDEX+1,
                    "startColumnIndex": START_COLUMN_INDEX,
                    "endColumnIndex": END_COLUMN_INDEX
                    },
                    #"pasteType": "PASTE_NORMAL".
                    "pasteType": "PASTE_VALUES",
                    "pasteOrientation": "NORMAL"
                }
            }
        ]
        # Write location to the sheet.
        bodyValues = [ self.location ]
        request =   service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range = SHEET_NAME + node_topic_range,
                    valueInputOption='USER_ENTERED',
                    body = {'values': [bodyValues]})
        try:
            request.execute()
        except:
            print('Write location to the sheet FAIL!')
            return

        print("Location   : " + self.location)
        self.location = "Unknown LOCATION!"

        # Write nodeInfo to the sheet.
        if (self.sensor == "DHT11" or self.sensor == "DHT22"):
            bodyValues = [ self.node_id, self.nodemcu, self.sensor] #DHT sensors
        else:
            bodyValues = [ self.node_id, self.nodemcu, self.sensor, self.alti] #BMP sensors

        request =   service.spreadsheets().values().update(
                    spreadsheetId = SPREADSHEET_ID,
                    range = SHEET_NAME + node_info_range,
                    valueInputOption = 'USER_ENTERED',
                    body = {'values': [bodyValues]})
        try:
            request.execute()
        except:
            print('Write nodeInfo to the sheet FAIL!')
            return

        print("NodeID     : " + self.node_id)
        print("NodeMcu    : " + self.nodemcu)
        print("Sensor     : " + self.sensor)
        #print("Altitude   : " + self.alti)
        print("Error count: " + self.failCount)
        #print("Vcc        : " + self.vcc)
        #self.node_id    = "Unknown NODE!"
        #self.nodemcu    = "Unknown MCU!"
        #self.sensor     = "Unknown SENSOR!"
        #self.alti       = "N/A"
        #self.failCount  = "?"
        #self.vcc       = "N/A"

        if (self.sensor == "DHT11" or self.sensor == "DHT22"):
            if ( self.temp == ERROR_VALUE):
                print("ERROR VALUE: Sensor = ", self.sensor)
                #print("Humidity   :{:>7}".format(self.humid))
            else:
                # 1) copy and paste data area one row down
                request = service.spreadsheets().batchUpdate(
                spreadsheetId = SPREADSHEET_ID,
                body = {'requests': [batch_update_spreadsheet_request_body]})
                try:
                    response = request.execute()
                except:
                    print('copy and paste data area FAIL!')
                    return

                # 2) Update datetime and values to MIN_ROW
                bodyValues = [ self.datetime, self.temp, self.humid ] #temp and humid
                print("Temperature: {:>7}".format(self.temp))
                if (self.humid == ERROR_VALUE):
                    print("Humidity ERROR! ",self.humid)
                    bodyValues = [ self.datetime, self.temp ] #temp only
                else:
                    print("Humidity   :{:>7}".format(self.humid))

                result =    service.spreadsheets().values().update(
                            spreadsheetId = SPREADSHEET_ID,
                            range = value_range,
                            valueInputOption = 'USER_ENTERED',
                            body = {'values': [bodyValues]})
                try:
                    result.execute()
                except:
                    print('Update date, time and values to MIN_ROW FAIL!')
                    return
                self.temp = "N/A"
                self.humid = "N/A"

                # 3) Clear row MAX_ROW+1
                #TODO: Do we need this at all?
                request =   service.spreadsheets().values().clear(
                            spreadsheetId = SPREADSHEET_ID,
                            range = (SHEET_NAME + '!A'+ str(MAX_ROW+1) + ':' + 'O' + str(MAX_ROW+1)))
                try:
                    request.execute()
                except:
                    print('Clear row MAX_ROW+1 FAIL!')
                    return

        elif (self.sensor == "BMP180" or self.sensor == "BMP180+ALS" or self.sensor == "BMP280" or self.sensor == "BMP280+ALS" or self.sensor == "BME280" or self.sensor == "BME280+ALS"):
            if ( self.temp == ERROR_VALUE or self.humid == ERROR_VALUE or self.baro == ERROR_VALUE ):
                print("ERROR VALUE, Sensor: ", self.sensor)
            else:
                # 1) copy and paste data area one row down
                request = service.spreadsheets().batchUpdate(
                spreadsheetId = SPREADSHEET_ID,
                body = {'requests': [batch_update_spreadsheet_request_body]})
                try:
                    response = request.execute()
                except:
                    print('copy and paste data area one row downFAIL!')
                    return

                # 2) Update date, time and values to MIN_ROW
                bodyValues = [ self.datetime, self.temp, self.baro] ##BMP180 & BMP280
                result =    service.spreadsheets().values().update(
                            spreadsheetId = SPREADSHEET_ID,
                            range = value_range,
                            valueInputOption = 'USER_ENTERED',
                            body = {'values': [bodyValues]})
                try:
                    result.execute()
                except:
                    print('Update date, time and values to MIN_ROW FAIL!')
                    return

                if (self.temp == "N/A"):
                    pass
                    #print("Temperature: ", self.temp)
                else:
                    print("Temperature: {:>7}".format(self.temp))
                if (self.baro == "N/A"):
                    pass
                    #print("Barometer  : ", self.baro)
                else:
                    print("Barometer  :{:>7}".format(self.baro))
                if (self.alti == "N/A"):
                    pass
                    #print("Altitude   : ", self.alti)
                else:
                    print("Altitude   :{:>7}".format(self.alti))
                if (self.humid == "N/A"):
                    pass
                    #print("Humidity   : ", self.humid)
                else:
                    print("Humidity   :{:>7}".format(self.humid))
                if (self.als == "N/A"):
                    pass
                    #print("Lightness  : ", self.als)
                else:
                    print("Lightness  :{:>7}".format(self.als))
                self.humid = "N/A"
                self.temp = "N/A"
                self.baro = "N/A"
                self.alti = "N/A"
                self.als = "N/A"

                # 3) Clear row MAX_ROW+1
                #TODO: Do we need this at all ?
                request =   service.spreadsheets().values().clear(
                            spreadsheetId=SPREADSHEET_ID,
                            range = (SHEET_NAME + '!A'+ str(MAX_ROW+1) + ':' + 'O' + str(MAX_ROW+1)))
                try:
                    request.execute()
                except:
                    print('Clear row MAX_ROW+1 FAIL!')
                    return

# Getters & Setters
    def getTemp(self):
        return self.temp
    def setTemp(self, temp):
        self.temp = temp

    def getHumid(self):
        return self.humid
    def setHumid(self, humid):
        self.humid = humid

    def getBaro(self):
        return self.baro
    def setBaro(self, baro):
        self.baro = baro

    def getAlti(self):
        return self.alti
    def setAlti(self, alti):
        self.alti = alti

    def getNodeID(self):
        return self.node_id
    def setNodeID(self, nodeID):
        self.node_id = nodeID

    def getFailCount(self):
        return self.failCount
    def setFailCount(self, failcount):
        self.failCount = failcount

    def getVcc(self):
        return self.vcc
    def setVcc(self, vcc):
        self.vcc = vcc

    def getNodeMcu(self):
        return self.nodemcu
    def setNodeMcu(self, nodemcu):
        self.nodemcu = nodemcu

    def getSensor(self):
        return self.sensor
    def setSensor(self, sensor):
        self.sensor = sensor

    def getLocation(self):
        return self.location
    def setLocation(self, location):
        self.location = location

    def getALS(self):
        return self.als
    def setALS(self, als):
        self.als = als

class Gredentials:
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first time.

    def __init__(self):
        self.creds = None

    def __del__(self):
       class_name = self.__class__.__name__

    def getToken(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token: pickle.dump(self.creds, token)

    def readToken(self):
        return self.token
