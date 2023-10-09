from pymongo import MongoClient
import sys
import time
import csv
import pandas as pd
from bson import Int64

import datetime
from bson.objectid import ObjectId

if __name__ == '__main__':

    for days in range(1, 30):
        client = MongoClient('mongo-0.qgraph-vpc.io:27000')
        app_id = sys.argv[1]

        profile = client[app_id]['profiles']
        events = client[app_id]['events']

        df = pd.DataFrame(events.find())

        print(profile)
        print(events)
        
        # df.to_csv('test' +'.csv', index=False ,columns=['userId','eventName','parameters'])

        # df = pd.DataFrame(profile.find({"gcmId" : {"$exists": True, "$ne": ""}}))

        # gen_time = datetime.datetime.today() - datetime.timedelta(days=days) 
        # dummy_id = ObjectId.from_datetime(gen_time)
        # result = list(events.find({"_id": {"$gte": dummy_id}}))

        # print("result: ", result)
        # df.to_csv('HomebookTable' +'.csv', index=False ,columns=['user_id','gcmId'])