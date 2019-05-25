#!/usr/bin/ python3

# ToDo: support for AmbientLightSensor TEMT6000
# ToDO: Baseline for ESP32 branch, cleanup
"""---------------------------- Version history --------------------------------
    v1.3    yasperzee   5'19    Remove DHT11 and DHT22 support
    v1.2.3  yasperzee   5'19    SleepTest
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

-----------------------------------------------------------------------------"""
import os.path
import pickle
import datetime

# Install Googleapiclient for python3 with pip3
from googleapiclient.discovery import build
# Install google-auth-oauthlib for python3 with pip3
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from configuration import *

class WriteNodeDataToSheet:

    def __init__(self):
        self.date       = "Empty!"
        self.time       = "Empty!"
        self.temp       = ERROR_VALUE
        self.humid      = ERROR_VALUE
        self.baro       = ERROR_VALUE
        self.alti       = ERROR_VALUE
        #self.light       = ERROR_VALUE
        self.failCount  = "?"
        self.vcc_batt   = "??"
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
        service = build('sheets', 'v4', credentials=self.creds)
        if service == 0:
            print('build FAIL!')

        spreadsheet = service.spreadsheets() # Returns the spreadsheets Resource.
        if spreadsheet == 0:
            print('service FAIL!')

        # set & print date & time
        d_format = "%d-%b-%Y"
        t_format = "%H:%M"
        now = datetime.datetime.today()
        self.date = now.strftime(d_format)
        self.time = now.strftime(t_format)
        print("\n" + self.date + " " + self.time )

        START_ROW_INDEX = MIN_ROW-1
        END_ROW_INDEX = MAX_ROW
        if self.node_id == "NODE-03":
            node_info_range  = node_info_range3
            node_topic_range = node_topic_range3
            value_range      = value_range3
            START_COLUMN_INDEX = 0
            END_COLUMN_INDEX   = 5
        else:
            print('Select Sensor!')

        # Write nodeInfo
        request =   service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range = SHEET_NAME + node_info_range,
                    valueInputOption='USER_ENTERED',
                    body={'values': [[ self.node_id, self.nodemcu, self.sensor]]})
        request.execute()
        print("NodeID     : " + self.node_id)
        print("NodeMcu    : " + self.nodemcu)
        print("Sensor     : " + self.sensor)

        # Write location and error count to 'node_topic_range_name'
        request =   service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range = SHEET_NAME + node_topic_range,
                    valueInputOption='USER_ENTERED',
                    body={'values': [[self.failCount, self.location ]]})
        request.execute()
        print("Location   :"  + self.location)
        print("Error count: " + self.failCount)

        if (self.sensor == "BMP180" or self.sensor == "BMP280"):
            if ( self.temp == ERROR_VALUE or self.baro == ERROR_VALUE or self.alti == ERROR_VALUE):
                print("ERROR VALUE, Sensor: ", self.sensor)
            else:
                # 1) copy and paste data area one row down
                batch_update_spreadsheet_request_body = [
                    {
                    "copyPaste": {
                        "source": {
                            "sheetId": SHEET_ID,
                            "startRowIndex": START_ROW_INDEX,
                            "endRowIndex": END_ROW_INDEX ,
                            "startColumnIndex": START_COLUMN_INDEX,
                            "endColumnIndex": END_COLUMN_INDEX
                            },
                        "destination": {
                            "sheetId": SHEET_ID,
                            "startRowIndex": START_ROW_INDEX+1,
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
                request =   service.spreadsheets().batchUpdate(
                            spreadsheetId=SPREADSHEET_ID,
                            body = {'requests': [batch_update_spreadsheet_request_body]})
                request.execute()

                # 2) Update date, time and values to MIN_ROW
                result =    service.spreadsheets().values().update(
                            spreadsheetId = SPREADSHEET_ID,
                            range= value_range,
                            valueInputOption='USER_ENTERED',
                            body={'values': [[ self.date, self.time, self.temp, self.baro, self.vcc_batt,self.alti ]]}) #BMP180 & BMP280
                result.execute()
                print("Temperature:{:>7}".format(self.temp))
                print("Barometer  :{:>7}".format(self.baro))
                print("Altitude   :{:>7}".format(self.alti))
                print("Vcc Batt   :{:>7}".format(self.vcc_batt))
                self.temp = ERROR_VALUE
                self.baro = ERROR_VALUE
                self.alti = ERROR_VALUE

                # 3) Clear row MAX_ROW+1
                request =   service.spreadsheets().values().clear(
                            spreadsheetId=SPREADSHEET_ID,
                            range = (SHEET_NAME + '!A'+ str(MAX_ROW+1) + ':' + 'O' + str(MAX_ROW+1)))
                request.execute()

    # Getters & Setters
    def getTime(self):
        return self.time
    def setTime(self, time):
        self.time = time

    def getDate(self):
        return self.date
    def setDate(self, date):
        self.date = date

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

    def getVccBatt(self):
        return self.vcc_batt
    def setVccBatt(self, vcc_batt):
        self.vcc_batt = vcc_batt

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
