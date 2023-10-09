import requests
import json
import sys
from datetime import datetime
from argparse import ArgumentParser

if __name__ == '__main__':

    parser = ArgumentParser(
        usage="python3 UI_overview.py <app_id> <apiToken>",
        description="This program will produce the report with the same data as UI")
    parser.add_argument("app_id", help="client's account app Id")
    parser.add_argument("apiToken", help="client's account API token")

    args = parser.parse_args()
    appId = args.app_id
    apiToken = args.apiToken

    url = 'https://aiqua.appier.com/qganalyzedata/overview/'

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Token %s" % apiToken,
        "appId": "%s" % appId
    }
    # request the endpoint
    res = requests.get(url, headers = headers)
    data = json.loads(res.text)
    web = data['web']['webAnalyticsByDailyUsers']
    

    f = open('%s.csv' % appId, 'w')
    f.writelines('device, browser, status, date, count\n')
    # construct the report 
    for dk, dv in web.items():
        device = dk
        for bk, bv in dv.items():
            browser = bk
            for sk, sv in bv.items():
                status = sk
                for entry in sv:
                    date = datetime.utcfromtimestamp(int(entry[0])).strftime('%Y-%m-%d')
                    count = entry[1]
                    f.writelines('%s,%s,%s,%s,%s\n' % (device, browser, status, date, count))
    f.close()

    if 'android' in data:
        android = data['android']['usersByUninstallDate']
        af = open('%s_android.csv' %appId, 'w')
        af.writelines('date, install, uninstall\n')
        
        for i in range(len(android[0])):
            date = datetime.utcfromtimestamp(int(android[0][i][0])).strftime('%Y-%m-%d')
            installCount = android[0][i][2]
            uninstallCount = android[0][i][1]
            af.writelines('%s,%s,%s\n' %(date, installCount, uninstallCount))
        af.close()
        
    if 'ios' in data:
        ios = data['ios']['usersByUninstallDate']
        iosf = open('%s_ios.csv' %appId, 'w')
        iosf.writelines('date, install, uninstall\n')
        
        for i in range(len(ios[0])):
            date = datetime.utcfromtimestamp(int(ios[0][i][0])).strftime('%Y-%m-%d')
            installCount = ios[0][i][2]
            uninstallCount = ios[0][i][1]
            iosf.writelines('%s,%s,%s\n' %(date, installCount, uninstallCount))
        iosf.close()
