from pymongo import MongoClient
import sys
import time
import csv
import pandas as pd
from bson import Int64

if __name__ == '__main__':

    client = MongoClient('mongodb://support:nMssHYRZ7kqc77uMKdao7QmOEGDt93KH@localhost:27017')
    app_id = sys.argv[1]

    # for members in ["user_id", "email", "phoneNo", "name", "allow_sms", "allow_edm", "type", "birthday"]:
    #     profile = client[ app_id +'_common']['profiles']
    #     if members == "platinum": status = "?~Y??~G~Q"
    #     elif members == "diamond": status = "?~Q??~_?"
    #     else: status = members
    #     df = pd.DataFrame(profile.find({'level':status,'source_channel':'寶島', 'birthday':{'$regex': '.*-02-.*'}}))
    #     df.to_excel('formosa_' + members +'.xlsx', index=False ,columns=['user_id','phoneNo','name','level', 'source_store_no', 'card_no', 'accept_sms'])
        # df.to_csv("寶島"+ members +'.csv',columns=['user_id','phoneNo','name','level', 'source_store_no', 'card_no", 'accept_sms''])

    profile = client[app_id]['profiles']
    user_detail = client[app_id]['user_details']
    event = client[app_id]['events']

    df = pd.DataFrame(user_detail.find({"appVer" : "2.3.0"}))

    if df.empty:
        print('Cannot find event')

    else:
        user_list2 = [Int64(i) for i in df.userId]

        result = pd.DataFrame(event.find({"userId": {'$in': user_list2},"eventName" : "notification_received"}))
        result.to_csv('Table' +'.csv', index=False ,columns=['userId'])

        # df.to_csv('AsoTable' +'.csv', index=False ,columns=['user_id','email','phoneNo','name', 'birthday', 'userId'])
        # df.to_excel('AsoTable' +'.xlsx', index=False ,columns=['user_id','email','phoneNo','name', 'allow_sms', 'allow_edm', 'type', 'birthday'])