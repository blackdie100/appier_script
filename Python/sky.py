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

    df = pd.DataFrame(events.find())
    df.to_csv('Sky' +'.csv', index=False ,columns=['userId','eventName'])
