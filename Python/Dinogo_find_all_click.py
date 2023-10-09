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
import json

def batch(list, n):
	start = 0
	while start < len(list):
		yield list[start: start+n]
		start += n

if __name__ == '__main__':

    # client = MongoClient('mongo-0.qgraph-vpc.io:27000')
    client = MongoClient('mongodb://support:nMssHYRZ7kqc77uMKdao7QmOEGDt93KH@localhost:27017')
    app_id = sys.argv[1]

    profile = client[app_id]['profiles']
    events = client[app_id]['events']
    user_detail = client[app_id]['user_details']

    df = pd.DataFrame(events.find({"parameters.notificationId" : Int64(6653330000), "eventName" : "notification_received"}))


    user_list2 = [Int64(i) for i in df.userId]

    # result = pd.DataFrame(user_detail.aggregate([{"$match": {"userId" : {'$in': user_list2}}},{"$group" :{"_id" : "$uninstallTime", "total" : {"$sum" : 1}}}]))

    # result = pd.DataFrame(profile.find({"userId": {'$in': user_list2}, "marketing_msg" : "N"}))
    result = pd.DataFrame(profile.find({"userId": {'$in': user_list2}, "uninstallTime" : {"$exists": True,"$ne":""}}))

    result.to_csv('test2.csv', index=False ,columns=['userId','uninstallTime'])

