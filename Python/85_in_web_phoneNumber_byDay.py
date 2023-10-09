from pymongo import MongoClient
import sys
import time
import csv
import pandas as pd
from bson import Int64

import pickle
import os.path
import json
from datetime import datetime,timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

import mysql.connector
import subprocess

SetSecond = 86400 # Set Second Interval
All_App_Id = ["3f7a5990e7cdd831255a_web"]

variable = []
variable2 = []
variable3 = []

def AccessMysql(query):
    mysql2 = mysql.connector.connect(
        host="ui-mysql.qgraph-vpc.io",
        user="readonlyuser",
        passwd="plaxieappiertw",
        database="qganalyzedata"
    )

    mycursor = mysql2.cursor()
    mycursor.execute(query)
    return mycursor.fetchone()

def Use85FTP(command):
    results = subprocess.run(command, shell=True, universal_newlines=True, check=True)

def job():
    if __name__ == '__main__':

        # client = MongoClient('mongo-1.qgraph-vpc.io:27000')
        client = MongoClient('mongodb://support:nMssHYRZ7kqc77uMKdao7QmOEGDt93KH@localhost:27017')
        global variable
        global variable2

        for app_id in All_App_Id:

            profile = client[app_id]['profiles']
            events = client[app_id]['events']
            user_detail = client[app_id]['user_details']

            RightNow = datetime.now() - timedelta(seconds=28800)
            RightNowAgo = datetime.now() - timedelta(seconds=SetSecond) - timedelta(seconds=28800)

            RightNowId = ObjectId.from_datetime(RightNow)
            RightNowAgoId = ObjectId.from_datetime(RightNowAgo)

            df = pd.DataFrame(events.find({"eventName" : "phoneNb_submit", '_id':{'$lt':RightNowId, '$gte': RightNowAgoId}, "parameters.phoneNo":{"$exists": True,"$ne":""}}, {'userId': 1, "parameters.phoneNo": 1, 'notificationId': 1}))

            if df.empty:
                print('Cannot find event by this campaign')

            else:
                # print(df)  ### following code has to add in else

                notificationId = df.notificationId.astype(str).str[0:6]
                PhoneNumber = df.parameters.astype(str).str[13:23]

                for notificationId2 in notificationId:

                    if 'nan' in notificationId2:
                        print('NaN in string! And use 778142')
                        notificationId2 = '778142'

                    query = 'select name from qganalyzedata_campaign where id=%s' % notificationId2
                    temp = list(AccessMysql(query))
                    variable.append(temp[0])
                    variable2.append(notificationId2)

                for PhoneNumber2 in PhoneNumber:
                    variable3.append(PhoneNumber2)

                notificationTitle = pd.DataFrame(data=variable, columns=["Campaign_Name"])
                notificationIdTitle = pd.DataFrame(data=variable2, columns=["Campaign_Id"])
                GetPhoneNumber = pd.DataFrame(data=variable3, columns=["Phone_Number"])

                if app_id is "3f7a5990e7cdd831255a_web":

                    df.insert(loc=2, column='Phone_Number', value=GetPhoneNumber)
                    df.insert(loc=3, column='Campaign_Name', value=notificationTitle)
                    df.insert(loc=4, column='Campaign_Id', value=notificationIdTitle)

                    df = df.drop_duplicates(subset='Phone_Number', keep='first')

                    if df.empty:
                        print('Final table is null')

                    else:
                        RightNow = datetime.now()
                        WebName = '/home/ubuntu/nick/85/'+'27617149_'+str(RightNow)[0:-15].replace(" ", "").replace(".", "").replace(":", "").replace("-", "")+'_Web.csv'

                        df.to_csv(WebName, index=False ,columns=['Phone_Number','Campaign_Name','Campaign_Id'])

                        WebFTPCommand = 'lftp -u appier_user,appierFTPpw08 -e "cd /Data/; put %s; quit" 60.199.195.86' % (WebName)
                        Use85FTP(WebFTPCommand)

print("Before run")
job()
print("Run finish")


