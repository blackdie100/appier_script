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

import mysql.connector
import subprocess

# CampaignID = [4379790000, 1111110000, 2222220000, 3333330000]  # Select Campaign ID
SetSecond = 3600 # Set Second Interval
All_App_Id = ["c0e48b50a24f174c218f_web"]

result_and = pd.DataFrame()
result_ios = pd.DataFrame()
result_and_exp = pd.DataFrame()
result_ios_exp = pd.DataFrame()
variable = []

def batch(list, n):
	start = 0
	while start < len(list):
		yield list[start: start+n]
		start += n

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
        global result_and
        global result_ios
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

            df = pd.DataFrame(profile.find({"wheel_campaign":"202011"}))
            # df = pd.DataFrame(events.aggregate([{"$match": {"eventName" : "qg_inapp_received"}},{"$group" :{"_id" : "$userId", "total" : {"$sum" : 1}}}]))

            # user_list2 = [Int64(i) for i in df.userId]
            # user_list2 = [Int64(i) for i in df._id]

            # result = pd.DataFrame(profile.aggregate([{"$match": {"userId" : {'$in': user_list2}}},{"$group" :{"_id" : "$gcmId", "total" : {"$sum" : 1}}}]))
            # result = pd.DataFrame(profile.find({"userId" : {'$in': user_list2}, "gcmId":{"$exists": True,"$ne":""}}, {'gcmId': 1}))

            print(df)

            df.to_csv("Dyaco.csv", index=False ,columns=['userId','email'])
            # print(result)

job()


