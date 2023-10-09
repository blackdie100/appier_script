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

CampaignID = [7104450000, 7104460000, 7100690000, 7100710000, 7100750000, 7100770000, 7100800000, 7100820000, 7100840000, 7100860000, 7100880000, 7100900000, 7100700000, 7100720000, 7100760000, 7100780000, 7100810000, 7100830000, 7100850000, 7100870000, 7100890000, 7100910000]  # Select Campaign ID
SetSecond = 3600 # Set Second Interval
All_App_Id = ["3f7a5990e7cdd831255a", "3f7a5990e7cdd831255a_ios"]

result_and = pd.DataFrame()
result_ios = pd.DataFrame()
result_and_exp = pd.DataFrame()
result_ios_exp = pd.DataFrame()
variable = []
variable2 = []

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
        global variable2

        for app_id in All_App_Id:

            profile = client[app_id]['profiles']
            events = client[app_id]['events']
            user_detail = client[app_id]['user_details']

            # RightNow = datetime.now() - timedelta(seconds=90600)
            # RightNowAgo = datetime.now() - timedelta(seconds=91200)

            RightNow = datetime.now() - timedelta(seconds=57360)
            RightNowAgo = datetime.now() - timedelta(seconds=64560)

            RightNowId = ObjectId.from_datetime(RightNow)
            RightNowAgoId = ObjectId.from_datetime(RightNowAgo)

            print(RightNow)
            print(RightNowAgo)

            # df = pd.DataFrame(events.find({"eventName" : "notification_clicked", '_id':{'$lt':RightNowId, '$gte': RightNowAgoId}}, {'userId': 1, "parameters.notificationId": 1}))


            for campaignID in CampaignID:
                df = pd.DataFrame(events.find({"eventName" : "notification_clicked", "parameters.notificationId" : Int64(campaignID), '_id':{'$lt':RightNowId, '$gte': RightNowAgoId}}, {'userId': 1, "parameters.notificationId": 1}))

                if df.empty:
                    print('Cannot find event by this campaign id=%s' % campaignID)

                else:
                    # print(df)  ### following code has to add in else

                    notificationId = df.parameters.astype(str).str[19:-5]

                    for notificationId2 in notificationId:
                        query = 'select name from qganalyzedata_campaign where id=%s' % notificationId2
                        temp = list(AccessMysql(query))
                        variable.append(temp[0])
                        variable2.append(notificationId2)

                    notificationTitle = pd.DataFrame(data=variable, columns=["Campaign_Name"])
                    notificationIdTitle = pd.DataFrame(data=variable2, columns=["Campaign_Id"])

                    if df.empty:
                        print('Data is empty!')

                    else:
                        user_list2 = [Int64(i) for i in df.userId]
                        result = pd.DataFrame()

                        
                        for users in batch(user_list2, 5000):
                            temp = pd.DataFrame(pd.json_normalize(profile.find({"userId": {'$in': users},"user_id":{"$exists": True,"$ne":""}}, {'user_id': 1, "parameters.notificationId": 1})))  #For ops server
                            # temp = pd.DataFrame(json_normalize(profile.find({"userId": {'$in': users}}, {'userId': 1, 'user_id': 1, "parameters.notificationId": 1}))) 
                            result = result.append(temp)

                            print("")
                            print(app_id + " in " + str(SetSecond) + " seconds ")

                        if result.empty:
                            print('Data is empty!')

                        else:
                            if app_id is "3f7a5990e7cdd831255a":
                                result_and_exp = pd.concat([result, result_and, result_and]).drop_duplicates(keep=False)

                                if result_and_exp.empty:
                                    print('all android data duplicated')

                                else:
                                    result_and_exp.insert(loc=2, column='Campaign_Name', value=notificationTitle)
                                    result_and_exp.insert(loc=3, column='Campaign_Id', value=notificationIdTitle)

                                    print(result_and_exp)

                                    # AndroidName = '/home/ubuntu/nick/85/'+str(RightNow).replace(" ", "_").replace(".", "_").replace(":", "_") +'_Android.csv'
                                    AndroidName = '/home/ubuntu/nick/85/'+'27617149_'+str(RightNow)[0:-13].replace(" ", "").replace(".", "").replace(":", "").replace("-", "")+'_test_Android2.csv'

                                    result_and_exp.to_csv(AndroidName, index=False ,columns=['user_id','Campaign_Name','Campaign_Id'])

                                    # AndroidFTPCommand = 'lftp -u appier_user,appierFTPpw08 -e "cd /Data/; put %s; quit" 60.199.195.86' % (AndroidName)
                                    # Use85FTP(AndroidFTPCommand)

                                    result_and = result

                            else:
                                result_ios_exp = pd.concat([result, result_ios, result_ios]).drop_duplicates(keep=False)

                                if result_ios_exp.empty:
                                    print('all ios data duplicated')

                                else:
                                    result_ios_exp.insert(loc=2, column='Campaign_Name', value=notificationTitle)
                                    result_ios_exp.insert(loc=3, column='Campaign_Id', value=notificationIdTitle)

                                    print(result_ios_exp)

                                    # iOSName = '/home/ubuntu/nick/85/'+str(RightNow).replace(" ", "_").replace(".", "_").replace(":", "_") +'_iOS.csv'
                                    iOSName = '/home/ubuntu/nick/85/'+'27617149_'+str(RightNow)[0:-13].replace(" ", "").replace(".", "").replace(":", "").replace("-", "")+'_test_iOS2.csv'

                                    result_ios_exp.to_csv(iOSName, index=False ,columns=['user_id','Campaign_Name','Campaign_Id'])

                                    # iOSFTPCommand = 'lftp -u appier_user,appierFTPpw08 -e "cd /Data/; put %s; quit" 60.199.195.86' % (iOSName)
                                    # Use85FTP(iOSFTPCommand)

                                    result_ios = result
            variable = []
            variable2 = []

        # if x < 6:
        #     time.sleep(3600)

# x = 1
# while x <= 6:
#     job()
#     print("This's %d runs!" % (x))
#     x += 1

job()

