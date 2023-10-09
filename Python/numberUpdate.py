from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from datetime import datetime,timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '10M9p_wtd2pCXdZEUxOMATqHzNp5naC1UQNAcjGms-kM'
UPDATE_RANGE = 'optInNum!A10:C'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    scriptDirectory = os.path.dirname(os.path.realpath(__file__))
    pathFile = scriptDirectory + '/token.pickle'
    if os.path.exists(pathFile):
        with open(pathFile, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                scriptDirectory + '/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pathFile, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #result = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
    #availableSheets = result['sheets']
    todayDate = datetime.now()
    yesterdayDate = (datetime.now() - timedelta(days=1))
    todayId = ObjectId.from_datetime(todayDate)
    yesterdayId = ObjectId.from_datetime(yesterdayDate)
    client = MongoClient('mongo-0.qgraph-vpc.io:27000')


    sheetName = 'optInNum'
    dbName = 'b7b261b295e388bcf5a2_web'
    range_ = UPDATE_RANGE
    print(range_)
    # update the sheet
    info = client[dbName]['profiles']
    total = info.count({'gcmId': {'$exists': True, '$ne': ''}, 'uninstallTime': {'$exists': False}})
    table = client[dbName]['events']
    result = table.count({'eventName':'subscribed_to_webpush','_id':{'$lt':todayId, '$gte': yesterdayId}})
    ##result = table.count({'gcmId': {'$exists': True, '$ne': ''}, 'uninstallTime': {'$exists': False}})
            #vapidCount = 0
            #nonVapidCount = 0
            #for user in result:
            #    if 'subscription' in user and 'subscriptionType' in user['subscription'] and user['subscription']['subscriptionType'] == 'vapid':
            #        vapidCount += 1
            #    else:
            #        nonVapidCount += 1
            #    total = vapidCount + nonVapidCount
    data = {
            "range": range_,
            "majorDimension": "ROWS",
            "values": [
            [todayDate.strftime('%Y-%m-%d'),result,total,todayDate.strftime('%Y-%m-%d')]
            ]
        }
    service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=range_, valueInputOption='RAW', insertDataOption='OVERWRITE', body=data).execute()
    print(result,total,todayDate.strftime('%Y-%m-%d'))

if __name__ == '__main__':
    main()
