import requests
from datetime import datetime,timedelta


NowTime = datetime.now() + timedelta(seconds=28800)
NowTimestamp = datetime.timestamp(NowTime)

medicinal_food_StartTime = NowTime - timedelta(seconds=21600)
medicinal_food_EndTime = NowTime
medicinal_food_StartTimestamp = datetime.timestamp(medicinal_food_StartTime)
medicinal_food_EndTimestamp = datetime.timestamp(medicinal_food_EndTime)


Active = '11' ## 0 is inactive, 11 is active
PercentString = '100%'

medicinal_food_url = "https://aiqua.appier.com/qganalyzedata/v2/campaigns/794103/"

medicinal_food_payload = '{\n    \"active\": \"%s\",\n    \"id\": 794103,\n    \"type1\": \"inweb\",\n    \"name\": \"medicinal_food\",\n    \"description\": \"Monday_Sunday_17pm_23pm\",\n    \"channel\": \"push\",\n    \"type\": \"web\",\n    \"include_segments\": [\n        111172\n    ],\n    \"exclude_segments\": [],\n    \"segment\": 111172,\n    \"includesegment\": null,\n    \"excludesegment\": null,\n    \"creative\": {\n        \"type\": \"inweb\",\n        \"triggerType\": \"scrollThreshold\",\n        \"startTime\": %d,\n        \"endTime\": %d,\n        \"include_new_users\": true,\n        \"whenCond\": {\n            \"eventName\": \"page_viewed\",\n            \"operator\": \"AND\",\n            \"conditions\": [\n                {\n                    \"value\": \"/SpecialNew\",\n                    \"param\": \"url\",\n                    \"op\": \"contains\"\n                }\n            ]\n        },\n        \"scheduledType\": \"once\",\n        \"maxNumTimesToShow\": 1,\n        \"audiencePlatform\": {\n            \"android\": true,\n            \"ios\": true,\n            \"others\": true\n        },\n        \"abCreativeVariants\": [\n            {\n                \"creativeType\": \"html\",\n                \"variantName\": \"Variant 1\",\n                \"maxLeadSubmitCount\": 1,\n                \"html\": {\n                    \"htmlBody\": \"<div class=\\\"aiqua\\\">\\r\\n                              <img src=\\\"https://cdn.qgraph.io/img/hosting/6f8b1ea135c988f5f915/1S0ObleAjm7xbleub4uL1m7O1S7O1lerbmkL1owUEmwvVSwM1m8OblULboe.png\\\">\\r\\n                              <div class=\\\"aiqua__content\\\">\\r\\n        <div class=\\\"aiqua__title\\\">十全安心藥膳燉包</div>\\r\\n                                  <div class=\\\"aiqua__message\\\">天氣冷颼颼，回到家，如果有熱呼呼的藥膳火鍋可以吃，真的是對心靈最大的安慰🥰十全藥膳燉包，湯頭甘甜滋補，順口好喝，只要簡單步驟，暖心十全大補湯輕鬆完成。</div>\\r\\n                                  <div class=\\\"aiqua__button\\\">\\r\\n            <a href=\\\"https://greenbox.tw/Products/SpecialNew/56983\\\">新品優惠中</a>\\r\\n                                   </div>\\r\\n    </div>\\r\\n</div>\\r\\n\\r\\n<style>\\r\\n.aiqua {\\r\\n    background-color: #fff;\\r\\n    max-width: 300px;\\r\\n                               border-radius: 5px;\\r\\n    overflow: hidden;\\r\\n}\\r\\n\\r\\n.aiqua > img {\\r\\n  width: %s;\\r\\n}\\r\\n\\r\\n.aiqua                            .aiqua__content {\\r\\n  padding: 0 20px 30px;\\r\\n}\\r\\n\\r\\n.aiqua .aiqua__content .aiqua__title {\\r\\n  font-family: OpenSans;\\r\\n                             font-size: 20px;\\r\\n  font-weight: 600;\\r\\n  color: #000;\\r\\n  white-space: initial;\\r\\n  margin: 10px 0 20px;\\r\\n}\\r\\n\\r\\n.aiqua .aiqua__content                            .aiqua__message {\\r\\n  font-family: OpenSans;\\r\\n  font-size: 14px;\\r\\n  color: #000;\\r\\n  white-space: initial;\\r\\n                             margin: 0 0 30px 0;\\r\\n}\\r\\n\\r\\n.aiqua .aiqua__content .aiqua__button {\\r\\n  font-family: OpenSans;\\r\\n  font-size: 14px;\\r\\n                             font-weight: 600;\\r\\n  text-align: center;\\r\\n  color: #fff;\\r\\n  line-height: 40px;\\r\\n  border-radius: 5px;\\r\\n                             background-color: #ff0000;\\r\\n  cursor: pointer;\\r\\n}\\r\\n\\r\\n.aiqua .aiqua__content .aiqua__button a {\\r\\n  color: #fff;\\r\\n                             text-decoration: none;\\r\\n}\\r\\n</style>\",\n                    \"showOverlay\": true\n                }\n            }\n        ],\n        \"isAB\": false,\n        \"scrollTriggerRule\": {\n            \"percent\": 10\n        }\n    },\n    \"event\": \"nothing\",\n    \"trigger\": \"nothing\",\n    \"stats\": {},\n    \"account\": \"2400\"\n}' % (Active, int(medicinal_food_StartTimestamp), int(medicinal_food_EndTimestamp), PercentString)

headers = {
  'Authorization': 'Token 09854576497642d92f277604e7d18dce184d257c',
  'appId': '6f8b1ea135c988f5f915',
  'Content-Type': 'application/json',
  'Cookie': '__cfduid=d327e10d9470901dd2a775ab4949a27051607496684'
}

medicinal_food_response = requests.request("PUT", medicinal_food_url, headers=headers, data = medicinal_food_payload.encode('utf-8'))

print(medicinal_food_response.text.encode('utf8'))



