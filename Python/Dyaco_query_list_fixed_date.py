from pymongo import MongoClient
import sys
import time
import csv
import pandas as pd
from bson import Int64
import pickle
import os.path
from datetime import datetime,timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from pandas.io.json import json_normalize
import os

def batch(list, n):
	start = 0
	while start < len(list):
		yield list[start: start+n]
		start += n

if __name__ == '__main__':


    client = MongoClient('mongodb://support:nMssHYRZ7kqc77uMKdao7QmOEGDt93KH@localhost:27017')
    app_id = sys.argv[1]

    profile = client[app_id]['profiles']
    events = client[app_id]['events']
    user_detail = client[app_id]['user_details']

    RightNow = datetime.strptime('2020-12-21',"%Y-%m-%d")
    RightNow = RightNow.replace(minute=00, hour=00, second=00, year=2020, month=12, day=21)

    RightNowAgo = datetime.strptime('2020-12-02',"%Y-%m-%d")
    RightNowAgo = RightNowAgo.replace(minute=00, hour=00, second=00, year=2020, month=12, day=2)

    RightNowId = ObjectId.from_datetime(RightNow)
    RightNowAgoId = ObjectId.from_datetime(RightNowAgo)

    df = pd.DataFrame(profile.find({'wheel_campaign':'202012', '_id':{'$lt':RightNowId, '$gte': RightNowAgoId}}, {'userId': 1, 'email': 1}))
    
    df.to_csv('List.csv', index=False ,columns=['userId','email'])
