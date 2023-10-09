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

SetSecond = 604800 # Set Second Interval
All_App_Id = ["6f17aaddbd8bb329f3eb", "6f17aaddbd8bb329f3eb_ios"]

result_and_exp = pd.DataFrame()
result_ios_exp = pd.DataFrame()
variable = []

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


def job():
    if __name__ == '__main__':

        # client = MongoClient('mongo-1.qgraph-vpc.io:27000')
        client = MongoClient('mongodb://support:nMssHYRZ7kqc77uMKdao7QmOEGDt93KH@localhost:27017')
        global result_and_exp
        global result_ios_exp
        global variable

        for app_id in All_App_Id:

            profile = client[app_id]['profiles']
            events = client[app_id]['events']
            user_detail = client[app_id]['user_details']

            RightNow = datetime.now()
            RightNowAgo = datetime.now() - timedelta(seconds=SetSecond)

            RightNowId = ObjectId.from_datetime(RightNow)
            RightNowAgoId = ObjectId.from_datetime(RightNowAgo)

            # df = pd.DataFrame(pd.json_normalize(events.find({"eventName" : "product_viewed", '_id':{'$lt':RightNowId, '$gte': RightNowAgoId}}, {'eventName':1, 'userId': 1, "parameters": 1})))
            # df2 = pd.DataFrame(pd.json_normalize(events.find({"eventName" : "checkout_completed", '_id':{'$lt':RightNowId, '$gte': RightNowAgoId}}, {'eventName':1, 'userId': 1, "parameters": 1})))

            df = pd.DataFrame(events.find({"eventName" : "product_viewed", '_id':{'$lt':RightNowId, '$gte': RightNowAgoId}}, {'eventName':1, 'userId': 1, "parameters": 1}))
            df2 = pd.DataFrame(events.find({"eventName" : "product_purchased", '_id':{'$lt':RightNowId, '$gte': RightNowAgoId}}, {'eventName':1, 'userId': 1, "parameters": 1}))
            df3 = pd.DataFrame(events.find({"eventName" : "app_launched", '_id':{'$lt':RightNowId, '$gte': RightNowAgoId}}, {'eventName':1, 'userId': 1, "parameters": 1}))

            result = pd.DataFrame()
            result = result.append(df)
            result = result.append(df2)
            result = result.append(df3)

            for getId in result['_id']:
                temp = getId.generation_time
                timestampStr = temp.strftime("%d-%b-%Y-%H:%M:%S")
                variable.append(timestampStr)

            DateFromObjID = pd.DataFrame(data=variable, columns=["Date"])

            print(app_id)

            if result.empty:
                print('Data is empty!')

            else:
                if app_id is "6f17aaddbd8bb329f3eb":

                    result_and_exp = result
                    result_and_exp.insert(loc=1, column='Date', value=DateFromObjID)

                    print(result_and_exp)

                    AndroidName = '/home/ubuntu/nick/lafresh/'+str(RightNow)[0:-13].replace(" ", "").replace(".", "").replace(":", "").replace("-", "")+'_Android.csv'
                    result_and_exp.to_csv(AndroidName, index=False ,columns=['Date','userId','eventName','parameters'])

                    email("lucas.chao@appier.com","Events record in Android","The attachment is the events record before 7 days",AndroidName)
                    email("kevin.cheng@lafresh.com.tw","Events record in Android","The attachment is the events record before 7 days",AndroidName)
                    email("hgsleo2000@lafresh.com.tw","Events record in Android","The attachment is the events record before 7 days",AndroidName)
                    email("nick.tsai@appier.com","Events record in Android","The attachment is the events record before 7 days",AndroidName)

                else:

                    result_ios_exp = result
                    result_ios_exp.insert(loc=1, column='Date', value=DateFromObjID)

                    print(result_ios_exp)

                    iOSName = '/home/ubuntu/nick/lafresh/'+str(RightNow)[0:-13].replace(" ", "").replace(".", "").replace(":", "").replace("-", "")+'_iOS.csv'
                    result_ios_exp.to_csv(iOSName, index=False ,columns=['Date','userId','eventName','parameters'])

                    email("lucas.chao@appier.com","Events record in iOS","The attachment is the events record before 7 days",iOSName)
                    email("lkevin.cheng@lafresh.com.tw","Events record in iOS","The attachment is the events record before 7 days",iOSName)
                    email("hgsleo2000@lafresh.com.tw","Events record in iOS","The attachment is the events record before 7 days",iOSName)
                    email("nick.tsai@appier.com","Events record in iOS","The attachment is the events record before 7 days",iOSName)
job()



