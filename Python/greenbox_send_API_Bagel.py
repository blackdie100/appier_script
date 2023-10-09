import requests
from datetime import datetime,timedelta


NowTime = datetime.now() + timedelta(seconds=28800)
NowTimestamp = datetime.timestamp(NowTime)

Bagel_StartTime = NowTime - timedelta(seconds=25200)
Bagel_EndTime = NowTime + timedelta(seconds=7200)
Bagel_StartTimestamp = datetime.timestamp(Bagel_StartTime)
Bagel_EndTimestamp = datetime.timestamp(Bagel_EndTime)


Active = '11' ## 0 is inactive, 11 is active
PercentString = '100%'
String = '春季必買的貝果，採用天然酵母製作，100%無添加，拒絕防腐劑及乳化劑，吃的美味又安心。'

Bagel_url = "https://aiqua.appier.com/qganalyzedata/v2/campaigns/1008856/"

Bagel_payload = '{\n    \"active\": \"%s\",\n    \"id\": 1008856,\n    \"type1\": \"inweb\",\n    \"name\": \"Bagel\",\n    \"description\": \"Monday_Sunday_14pm_23pm!!!\",\n    \"channel\": \"push\",\n    \"type\": \"web\",\n    \"include_segments\": [\n        111172\n    ],\n    \"exclude_segments\": [],\n    \"segment\": 111172,\n    \"includesegment\": null,\n    \"excludesegment\": null,\n    \"creative\": {\n        \"type\": \"inweb\",\n        \"triggerType\": \"scrollThreshold\",\n        \"startTime\": %d,\n        \"endTime\": %d,\n        \"include_new_users\": true,\n        \"whenCond\": {\n            \"eventName\": \"page_viewed\",\n            \"operator\": \"AND\",\n            \"conditions\": [\n                {\n                    \"value\": \"/SpecialNew\",\n                    \"param\": \"url\",\n                    \"op\": \"contains\"\n                }\n            ]\n        },\n        \"scheduledType\": \"once\",\n        \"maxNumTimesToShow\": 1,\n        \"audiencePlatform\": {\n            \"android\": true,\n            \"ios\": true,\n            \"others\": true\n        },\n        \"abCreativeVariants\": [\n            {\n                \"creativeType\": \"html\",\n                \"variantName\": \"Variant 1\",\n                \"maxLeadSubmitCount\": 1,\n                \"html\": {\n                    \"htmlBody\": \"<div class=\\\"aiqua\\\">\\r\\n                              <img src=\\\"https://cdn.qgraph.io/img/hosting/6f8b1ea135c988f5f915/1S0rbS8-jS2Jjm5xbhuL1m7r1m7rjSeubm0l1mwB1S0rbS8-jS2Jjk.jpg\\\">\\r\\n                              <div class=\\\"aiqua__content\\\">\\r\\n        <div class=\\\"aiqua__title\\\">【3天100組銷售一空】超夯貝果進貨囉！</div>\\r\\n                                  <div class=\\\"aiqua__message\\\">%s</div>\\r\\n                                  <div class=\\\"aiqua__button\\\">\\r\\n            <a href=\\\"https://greenbox.tw/Products/ItemDetail/57582\\\">來去搶購></a>\\r\\n                                   </div>\\r\\n    </div>\\r\\n</div>\\r\\n\\r\\n<style>\\r\\n.aiqua {\\r\\n    background-color: #fff;\\r\\n    max-width: 300px;\\r\\n                               border-radius: 5px;\\r\\n    overflow: hidden;\\r\\n}\\r\\n\\r\\n.aiqua > img {\\r\\n  width: %s;\\r\\n}\\r\\n\\r\\n.aiqua                            .aiqua__content {\\r\\n  padding: 0 20px 30px;\\r\\n}\\r\\n\\r\\n.aiqua .aiqua__content .aiqua__title {\\r\\n  font-family: OpenSans;\\r\\n                             font-size: 20px;\\r\\n  font-weight: 600;\\r\\n  color: #000;\\r\\n  white-space: initial;\\r\\n  margin: 10px 0 20px;\\r\\n}\\r\\n\\r\\n.aiqua .aiqua__content                            .aiqua__message {\\r\\n  font-family: OpenSans;\\r\\n  font-size: 14px;\\r\\n  color: #000;\\r\\n  white-space: initial;\\r\\n                             margin: 0 0 30px 0;\\r\\n}\\r\\n\\r\\n.aiqua .aiqua__content .aiqua__button {\\r\\n  font-family: OpenSans;\\r\\n  font-size: 14px;\\r\\n                             font-weight: 600;\\r\\n  text-align: center;\\r\\n  color: #fff;\\r\\n  line-height: 40px;\\r\\n  border-radius: 5px;\\r\\n                             background-color: #ff0000;\\r\\n  cursor: pointer;\\r\\n}\\r\\n\\r\\n.aiqua .aiqua__content .aiqua__button a {\\r\\n  color: #fff;\\r\\n                             text-decoration: none;\\r\\n}\\r\\n</style>\",\n                    \"showOverlay\": true\n                }\n            }\n        ],\n        \"isAB\": false,\n        \"scrollTriggerRule\": {\n            \"percent\": 10\n        }\n    },\n    \"priority\": 2,\n    \"event\": \"nothing\",\n    \"trigger\": \"nothing\",\n    \"stats\": {\n        \"total_seg_duration\": 0,\n        \"pid\": \"14216\",\n        \"detailedLog\": \"http://internal.aiqua.appier.info/log/crunner-inweb/toggle/detailed-log/2021-03-16/20210316-020601-1008856-2400.txt\",\n        \"total_records\": 2,\n        \"logFilePath\": \"http://internal.aiqua.appier.info/log/crunner-inweb/toggle/log/2021-03-16/20210316-020601-1008856-2400.txt\",\n        \"campaign_start_time\": \"2021-03-16 02:06:01\"\n    },\n    \"account\": \"2400\"\n}' % (Active, int(Bagel_StartTimestamp), int(Bagel_EndTimestamp),String, PercentString)

headers = {
  'Authorization': 'Token 09854576497642d92f277604e7d18dce184d257c',
  'appId': '6f8b1ea135c988f5f915',
  'Content-Type': 'application/json',
  'Cookie': '__cfduid=df443e78b8522bc703fd2099de7ba92991615863739'
}

Bagel_response = requests.request("PUT", Bagel_url, headers=headers, data = Bagel_payload.encode('utf-8'))

print(Bagel_response.text.encode('utf8'))

