from pymongo import MongoClient
import sys
import time
import csv
import pandas as pd
from bson import Int64

if __name__ == '__main__':

    client = MongoClient('mongo-0.qgraph-vpc.io:27000')
    app_id = sys.argv[1]

    for members in ["platinum", "diamond", "EYE"]:
        profile = client[ app_id +'_common']['profiles']
        if members == "platinum": 
            status = "?~Y??~G~Q"
        elif members == "diamond": 
            status = "?~Q??~_?"
        else: 
            status = members
            
        df = pd.DataFrame(profile.find({'level':status,'source_channel':'寶島', 'birthday':{'$regex': '.*-02-.*'}}))
        df.to_excel('formosa_' + members +'.xlsx', index=False ,columns=['user_id','phoneNo','name','level', 'source_store_no', 'card_no', 'accept_sms'])
        # df.to_csv("寶島"+ members +'.csv',columns=['user_id','phoneNo','name','level', 'source_store_no', 'card_no", 'accept_sms''])