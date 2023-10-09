from pymongo import MongoClient
import sys
import time
import csv
import pandas as pd
from bson import Int64

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

if __name__ == '__main__':

    client = MongoClient('mongo-0.qgraph-vpc.io:27000')
    app_id = sys.argv[1]

    profile = client[app_id]['profiles']
    events = client[app_id]['events']

    for x in range(1, 6):

        todayDate = datetime.now()
        yesterdayDate = (datetime.now() - timedelta(days=x))

        todayId = ObjectId.from_datetime(todayDate)
        yesterdayId = ObjectId.from_datetime(yesterdayDate)

        result = events.count({'eventName':'product_clicked_fast_redirect','_id':{'$lt':todayId, '$gte': yesterdayId}})
        result2 = events.count({'eventName':'category_page_viewed','_id':{'$lt':todayId, '$gte': yesterdayId}})

        print(todayDate)
        print(yesterdayDate)

        print ("product_clicked_fast_redirect: ", result)
        print ("category_page_viewed: ",result2)


    # result = list(profile.find({"gcmId" : {"$exists": True, "$ne": ""}}).limit(5))
    # print(result)

    # df = pd.DataFrame(profile.find({"gcmId" : {"$exists": True, "$ne": ""}}))


    # for members in ["platinum", "diamond", "EYE"]:


    # df = pd.DataFrame(profile.find({"gcmId" : {"$exists": True, "$ne": ""}}))

    # gen_time = datetime.datetime.today() - datetime.timedelta(15) 
    # dummy_id = ObjectId.from_datetime(gen_time)
    # result = list(events.find({"_id": {"$gte": dummy_id}}).limit(5))

    # df.to_csv('HomebookTable' +'.csv', index=False ,columns=['user_id','gcmId'])
