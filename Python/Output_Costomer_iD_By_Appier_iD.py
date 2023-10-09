from pymongo import MongoClient
import sys
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

    #Variables
    FOLDERNAME = 'rcti'
    FILENAME = '123934.txt'
    OUTPUTNAME = 'rcti_Output_and.csv'

    filepath = '%s/%s' %(FOLDERNAME, FILENAME)
    output_filepath = '%s/%s' %(FOLDERNAME, OUTPUTNAME)

##### For Android #####
    with open(filepath , encoding="utf-8") as fp:
        user_list = fp.readlines()
        result = pd.DataFrame()

        for users in batch(user_list, 5000):
            user_list = [str(i).lower().strip('\n') for i in users] ## low case for aaid
            temp = pd.DataFrame(user_detail.find({"advInfo.aid": {'$in': user_list}}))
            result = result.append(temp)

        user_list2 = [Int64(i) for i in result.userId]
        df2 = pd.DataFrame(profile.find({"userId": {'$in': user_list2}})) ##Insert Appier userId

        df2.to_csv(output_filepath, index=False ,columns=['userId','aiq_push_enabled'])


##### For iOS #####
    # with open(filepath , encoding="utf-8") as fp:
    #     user_list = fp.readlines()
    #     user_list = [str(i).strip('\n') for i in user_list] 
    #     df = pd.DataFrame(user_detail.find({"IDFA": {'$in': user_list}}))

    #     user_list2 = [Int64(i) for i in df.userId]
    #     df2 = pd.DataFrame(profile.find({"userId": {'$in': user_list2}})) ##Insert Appier userId

    #     df2.to_csv(output_filepath, index=False ,columns=['userId','aiq_push_enabled'])

        
##### For Web #####
    # with open(filepath , encoding="utf-8") as fp:
    #     user_list = fp.readlines()
    #     user_list = [str(i).strip('\n') for i in user_list] 

    #     # user_list2 = [Int64(i) for i in user_list]

    #     df = pd.DataFrame(profile.find({"wUserId": {'$in': user_list}})) ##Insert Appier userId

    #     if df.empty:
    #         print('Cannot find event')

    #     else:
    #         df.to_csv(output_filepath, index=False ,columns=['userId','wUserId'])








