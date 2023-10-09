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

    client = MongoClient('mongo-0.qgraph-vpc.io:27000')
    app_id = sys.argv[1]

    profile = client[app_id]['profiles']
    events = client[app_id]['events']
    user_detail = client[app_id]['user_details']

    df = pd.DataFrame(profile.find({"gcmId":{"$exists": True,"$ne":""},"uninstallTime":{"$exists": False}}, {'userId': 1}))

    user_list2 = [Int64(i) for i in df.userId]
    result = pd.DataFrame(user_detail.aggregate([{"$match": {"userId" : {'$in': user_list2}}},{"$group" :{"_id" : "$appVer", "total" : {"$sum" : 1}}}]))

    print(result)
