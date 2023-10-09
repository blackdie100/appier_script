import mysql.connector
import subprocess

from datetime import datetime,timedelta

def AccessMysql(query):
    mysql2 = mysql.connector.connect(
        host="ui-mysql.qgraph-vpc.io",
	    user="ui-backend",
	    passwd="QgRaPh@i23",
	    database="qganalyzedata"
    )

    mycursor = mysql2.cursor()
    mycursor.execute(query)

    mysql2.commit()


NowTime = datetime.now() + timedelta(seconds=28800)
StartTime = NowTime + timedelta(seconds=3600)
EndTime = NowTime + timedelta(seconds=54000)

NowTimestamp = datetime.timestamp(NowTime)
StartTimestamp = datetime.timestamp(StartTime)
EndTimestamp = datetime.timestamp(EndTime)

CampaignId = "249076"
# CampaignHTMLBody = '{"htmlBody": "<div class=\\"aiqua\\">\\r\\n    <a class=\\"aiqua__item-link\\">\\r\\n      \
# <img class=\\"aiqua__item-img\\" src=\\"https://cdn.qgraph.io/img/hosting/6f8b1ea135c988f5f915/1S0ObleJjS7lbo\
# 2xjh-8sS8xblP8sS0xPSg8sS2rbF38sS2O1mK8sS5lbmT8sS5APFP8sS5A1SPWd95xPF5xd95JPogod95x1lkOd95xbM3c7mwB1S0ObleJjS\
# 7lbO.jpg\\" alt=\\"\\" />\\r\\n    </a>\\r\\n</div>\\r\\n\\r\\n\\r\\n<style>\\r\\n.aiqua {\\r\\n    max-width: 500px;\\r\\n    ov\
# erflow: hidden;\\r\\n}\\r\\n\\r\\n.aiqua .aiqua__item-img {\\r\\n  width: 100%;\\r\\n}\\r\\n</style>", "showOverlay": false}'

CampaignCreative = '{"type": "inweb", "triggerType": "userEvent", "startTime": %d, "endTime": %d, \
"include_new_users": false, "whenCond": {"eventName": "product_viewed", "operator": "AND", "conditions": []}, "creativeType": \
"lead", "scheduledType": "repeats", "maxNumTimesToShow": 100, "maxLeadSubmitCount": 1, "audiencePlatform": {"android": false, \
"ios": false, "others": true}, "lead": {"inputs": [{"fieldName": "email", "placeholder": "Email", "inputType": "text", \
"dataType": "string", "required": true}], "agreementUrl": "", "imgSrc": "", "title": "Test", "message": "Test", "submitText": \
"Submit", "redirectUrl": "", "titleColor": "#000", "messageColor": "#000", "agreementText": "I have read and agreed to the \
terms of Use and Personal Information", "agreementColor": "#0090ff", "submitColor": "#fff", "submitBackgroundColor": "#0090ff", \
"contentBackgroundColor": "#fff", "showOverlay": true, "errorMessages": {"required": "This field is required", "invalid": \
"Invalid value", "agreement": "Please tick above to agree terms"}}}' % (int(StartTimestamp), int(EndTimestamp))

# CampaignCreative = '{"type": "inweb", "triggerType": "scrollThreshold", "startTime": %d, "endTime": %d, \
# "include_new_users": true, "whenCond": {"eventName": "page_viewed", "operator": "AND", "conditions": \
# [{"value": "/SpecialNew", "param": "url", "op": "contains"}]}, "scheduledType": "once", "maxNumTimesToSho\
# w": 1, "audiencePlatform": {"android": true, "ios": true, "others": true}, "isAB": false, "scrollTriggerRule": \
# {"percent": 10}, "creativeType": "html", "maxLeadSubmitCount": 1, "html": %s}' % (int(StartTimestamp), int(EndTimestamp), CampaignHTMLBody)

query = "update qganalyzedata_campaign set creative='%s' where id=%s;" % (CampaignCreative, CampaignId)

print(query)
AccessMysql(query)






