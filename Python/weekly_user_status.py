from pymongo import MongoClient
import requests
import sys
import os
import time
import csv
import json
import pandas as pd
from bson import Int64
import base64

if __name__ == '__main__':

    client = MongoClient('mongo-0.qgraph-vpc.io:27000')
    app_id = '3247768a07e29b6c3e77'
    profile = client[ app_id + '_common' ]['profiles']
    profile_df =  pd.DataFrame(profile.find())

    for platform in ['_web','','_ios']:
        profile = client[ app_id + platform ]['profiles']
        tmp_df = pd.DataFrame(profile.find())
        profile_df = pd.concat( [ profile_df , tmp_df ], ignore_index = True, sort = True )

    profile_df.drop_duplicates( 'email' , 'first' , inplace= True )
    scriptDirectory = os.path.dirname(os.path.realpath(__file__)) + "/"
    profile_df.to_excel(scriptDirectory + "email_info.xlsx", index = False)

    # send the email
    sg_header = {
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json'
    }

    sg_url = 'https://api.sendgrid.com/v3/mail/send'

    with open(scriptDirectory + "email_info.xlsx", 'rb') as f:
        data = f.read()

    attachment = base64.b64encode(data)
    base64_string = attachment.decode('utf-8')

    content = {
        "personalizations": [
            {
                "to": [{"email": "tienyu.chang@appier.com"}, {"email": "louis.chu@appier.com"}, {"email": "ryan.yuan@appier.com"}, {"email": "stephanie.kuo@appier.com"}, {"email": "jennifer.huang@appier.com"}],
                "subject": "Weekly User Status Update"
            }
        ],
        "from": {
            "email": "info@maketing.appier.com"
        },
        "content": [
            {
                "type": "text/html",
                "value": "Please find the reports in the attachment."
            }
        ],
        "attachments": [
            {
                "filename": "weekly_user_status.xlsx",
                "content": base64_string
            }
        ]
    }

    sg_r = requests.post(sg_url, headers=sg_header, data=json.dumps(content))
    print(sg_r.text)
