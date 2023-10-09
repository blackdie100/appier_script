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
from pandas.io.json import json_normalize
import os

import requests
import base64

SetSecond = 86400 # Set Second Interval
SetSecond2 = 54000 # Set Second Interval

All_App_Id = ["bb1d895c2707ead042f7_web"]

DataArray = []
SubscribersArray = []
BlockedArray = []
CSubscribersArray = []

def email(emails, subject, content, attachment_origin_file_name=None, attachment_file_name=None):
    '''
        Send an email through Sendgrid. The sending address is alerts@qgraph.io.
        Returns the response text from the Sendgrid request
        - email_addresses: one address or a list of the destination email addresses \
            (as str variables)
        - subject: the subject of the email
        - content: the text content of the email
        Optional:
        - attachment_origin_file_name: the name of a file you want to \
        include as attachment (path/to/example.file)
        - attachment_file_name: the name that the attachment will have \
        in the email (same as origin name if blank, path is cut off)
    '''
    if type(emails) is str:
        emails = [{'email':emails}]
    else:
        emails = [{'email':e} for e in emails]
    # if no attachment file name, take that of the input file
    if attachment_origin_file_name is not None:
        if attachment_file_name is None:
            attachment_file_name = attachment_origin_file_name.rsplit('/', 1)[-1].rsplit('\\', 1)[-1]
            # (cut off path if there is a path before the file name)
    sg_header = {
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json'
    }
    sg_url = 'https://api.sendgrid.com/v3/mail/send'
    # read data and encode it in b64
    if attachment_origin_file_name is not None:
        with open(attachment_origin_file_name, 'rb') as f:
            data = f.read()
        attachment = base64.b64encode(data)
        base64_string = attachment.decode('utf-8')
    # Setting the content: see Sendgrid documentation for more detail
    content = {
        "personalizations": [
            {
                "to": emails,
                "subject": subject
            }
        ],
        "from": {
            "email": "alerts@qgraph.io"
        },
        "content": [
            {
                "type": "text/plain",
                "value": content
            }
        ]
    }
    if attachment_origin_file_name is not None:
        content["attachments"] = [{
                "filename": attachment_file_name,
                "content": base64_string
            }]
    sg_r = requests.post(sg_url, headers=sg_header, data=json.dumps(content))
    return sg_r.text


def parser(app_id, apiToken, path):
    appId = app_id
    apiToken = apiToken

    url = 'https://aiqua.appier.com/qganalyzedata/overview/'

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Token %s" % apiToken,
        "appId": "%s" % appId
    }
    # request the endpoint
    res = requests.get(url, headers = headers)
    data = json.loads(res.text)
    web = data['web']['webAnalyticsByDailyUsers']

    f = open('%s/%s.csv' % (path, appId), 'w')
    f.writelines('device, browser, status, date, count\n')
    # construct the report 
    for dk, dv in web.items():
        device = dk
        for bk, bv in dv.items():
            browser = bk
            for sk, sv in bv.items():
                status = sk
                for entry in sv:
                    date = datetime.utcfromtimestamp(int(entry[0])).strftime('%Y-%m-%d')
                    count = entry[1]
                    f.writelines('%s,%s,%s,%s,%s\n' % (device, browser, status, date, count))
    f.close()




def job():
    if __name__ == '__main__':

        # client = MongoClient('mongo-1.qgraph-vpc.io:27000')
        client = MongoClient('mongodb://support:nMssHYRZ7kqc77uMKdao7QmOEGDt93KH@localhost:27017')
        global DataArray
        global SubscribersArray
        global BlockedArray
        global NewuserArray

        for app_id in All_App_Id:

            ############################ Query Data From API ############################

            parser("bb1d895c2707ead042f7", "a72f5072a9a342d3552b5d30951e9b45440aec48", "/home/ubuntu/nick/HyRead")

            df1 = pd.read_csv("/home/ubuntu/nick/HyRead/bb1d895c2707ead042f7.csv")

            df1 = df1[df1['device'] == 'All Devices']
            df1 = df1[df1[" browser"] == 'All Browsers']

            df_Blocked = df1[df1[' status'] == 'Blocked']
            df_Subscribed = df1[df1[' status'] == 'Subscribed']

            getDate = pd.DataFrame(data=df_Blocked, columns=[" date"])
            getBlocked = pd.DataFrame(data=df_Blocked, columns=[" count"])
            getSubscribed = pd.DataFrame(data=df_Subscribed, columns=[" count"])

            getBlocked = getBlocked.rename(columns = {' count': 'Blocked'}, inplace = False)
            getSubscribed = getSubscribed.rename(columns = {' count': 'Subscribed'}, inplace = False)



            ############################ Caculate Data From Mongo ############################

            profile = client[app_id]['profiles']

            RightNow = datetime.now()
            Month = int(RightNow.strftime("%m")) - 1

            if(Month == 2 or Month == 4 or Month == 6 or Month == 9 or Month == 11):
                print("In 30 days")
                
                for i in range(1, 32):   ####Match the value size from querying API####
                    RightNowAfter = datetime.now() - timedelta(seconds=SetSecond*(i-1)) - timedelta(seconds=SetSecond2)
                    RightNowBefore = datetime.now() - timedelta(seconds=SetSecond*i) - timedelta(seconds=SetSecond2)

                    RightNowAfterId = ObjectId.from_datetime(RightNowAfter)
                    RightNowBeforeId = ObjectId.from_datetime(RightNowBefore)

                    # subscribers = pd.DataFrame(profile.find({"uninstallTime" : {'$exists': False}, "gcmId" : {'$exists': True, '$ne':""}, '_id':{'$lt':RightNowAfterId, '$gte': RightNowBeforeId}}, {'userId': 1}))
                    # blocked = pd.DataFrame(profile.find({"permission" : "denied" ,'_id':{'$lt':RightNowAfterId, '$gte': RightNowBeforeId}}, {'userId': 1}))
                    csubscribers = pd.DataFrame(profile.find({"uninstallTime" : {'$exists': False}, "gcmId" : {'$exists': True, '$ne':""}, '_id':{'$lt':RightNowAfterId}}, {'userId': 1}))

                    # DataArray.append(RightNowAfter.strftime("%Y-%m-%d"))
                    # SubscribersArray.append(subscribers.count()['_id'])
                    # BlockedArray.append(blocked.count()['_id'])
                    CSubscribersArray.append(csubscribers.count()['_id'])

            else:
                print("In 31 days")
                
                for i in range(1, 32):
                    RightNowAfter = datetime.now() - timedelta(seconds=SetSecond*(i-1)) - timedelta(seconds=SetSecond2)
                    RightNowBefore = datetime.now() - timedelta(seconds=SetSecond*i) - timedelta(seconds=SetSecond2)

                    RightNowAfterId = ObjectId.from_datetime(RightNowAfter)
                    RightNowBeforeId = ObjectId.from_datetime(RightNowBefore)

                    # subscribers = pd.DataFrame(profile.find({"uninstallTime" : {'$exists': False}, "gcmId" : {'$exists': True, '$ne':""}, '_id':{'$lt':RightNowAfterId, '$gte': RightNowBeforeId}}, {'userId': 1}))
                    # blocked = pd.DataFrame(profile.find({"permission" : "denied" ,'_id':{'$lt':RightNowAfterId, '$gte': RightNowBeforeId}}, {'userId': 1}))
                    csubscribers = pd.DataFrame(profile.find({"uninstallTime" : {'$exists': False}, "gcmId" : {'$exists': True, '$ne':""}, '_id':{'$lt':RightNowAfterId}}, {'userId': 1}))

                    # DataArray.append(RightNowAfter.strftime("%Y-%m-%d"))
                    # SubscribersArray.append(subscribers.count()['_id'])
                    # BlockedArray.append(blocked.count()['_id'])
                    CSubscribersArray.append(csubscribers.count()['_id'])
                    

            result_exp = getDate

            result_exp['Blocked'] = getBlocked.values
            result_exp['Subscribed'] = getSubscribed.values
            result_exp['Current Subscribers'] = CSubscribersArray[::-1]

            CSV_Name = '/home/ubuntu/nick/HyRead/'+'Result.csv'
            result_exp.to_csv(CSV_Name, index=False ,columns=[' date', 'Subscribed','Blocked','Current Subscribers'])

            email("nick.tsai@appier.com","HyRead monthly reminder","The attachment is the users record before one month",CSV_Name)
            email("mira.chu@appier.com","HyRead monthly reminder","The attachment is the users record before one month",CSV_Name)

job()



