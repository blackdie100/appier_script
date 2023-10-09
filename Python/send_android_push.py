# python 3
import sys
import json
import time
import gzip
import base64
import collections

from urllib.request import Request, urlopen
from argparse import ArgumentParser

def get_compressed_string(packet):
    assert isinstance(packet, collections.Mapping)
    data = bytes(json.dumps(packet), 'utf-8')
    compressed_string = gzip.compress(data)
    return str(base64.urlsafe_b64encode(compressed_string), 'utf-8')


def _fcm_send(key, data):
    fcm_url = 'https://fcm.googleapis.com/fcm/send'
    # fcm_url = 'https://android.googleapis.com/gcm/send'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=%s' % (key),
    }
    # for python 3, encode data
    data = data.encode('utf-8')
    request = Request(fcm_url, data, headers)
    response = urlopen(request)
    result = response.read().decode("utf-8")
    # FIXME: broken for bulk results
    if result.startswith("Error="):
        print('error')
    return result


def send_message(fcm_key, fcm_ids, msg):
    values = {
        'registration_ids': fcm_ids,
        'data': {'message': msg},
        'priority': 'high',
        'collapse_key': 'r_t_ft'
    }

    return _fcm_send(fcm_key, json.dumps(values))


def send_push(fcm_key, data):
    key = fcm_key

    users = data.get('users', [])
    if not users:
        raise Exception('no users provided')

    title = data.get('title', 'default title')
    message = data.get('message', 'default message')

    if not len(users) > 0:
        return 0, 'no users present'

    message_json = {
        'source': 'QG',
        'title': title,
        'message': message,
        'notificationId': 123,
        'type': data['type'],
        'pileUp' :  True,
        'channelId': 'po',
        'rno': int(time.time()),
        'dry_run': True
    }

    if 'dynamic' in data:
        message_json['dynamic'] = data['dynamic']

    if 'iconUrl' in data:
        message_json['imageUrl'] = data['iconUrl']
    if 'bigImgUrl' in data:
        message_json['bigImageUrl'] = data['bigImgUrl']
    if 'action1' in data:
        message_json['actions'] = []
        message_json['actions'].append({'text': data['action1'], 'id': 1})
        message_json['actions'].append({'text': data['action2'], 'id': 2})
        message_json['actions'].append({'text': data['action3'], 'id': 3})

    gcmIds = []
    success_cnt = 0
    for user in users:
        gcmIds.append(user['gcmId'])
    ret_message = send_message(
                    key,
                    gcmIds,
                    message_json
                )
    ret_message = json.loads(ret_message)
    if 'success' in ret_message:
        success_cnt += ret_message['success']
    return success_cnt, ret_message

if __name__ == '__main__':

    parser = ArgumentParser(
        usage="python3 send_android_push.py <fcm_key> <gcmId>",
        description="This program will try to send a real push to the designated device.")
    parser.add_argument("fcm_key", help="client's FCM key")
    parser.add_argument("gcmId", help="user's FCM token")

    args = parser.parse_args()
    fcm_key = args.fcm_key
    fcm_token = args.gcmId

    dynamic_payload = {
        "std": 0,
        "values": {
            "title": "Custom Push Title",
            "message": "This is test message for custom push",
            "deeplink": "https://www.google.com",
            "isicon2": "url_icon_st_centerCrop",
            "isimage": "url_image_st_centerCrop",
            "tstitle": "txt_title_ls_1_al_left_tc_#000000_s_15_tf_b",
            "tsmessage": "txt_message_tc_#000000_ls_2_s_13_al_left",
            "tt": "",
            "tsbkgrnd": "txt_tt_bc_#ffffff",
            "icon": "https://img11.androidappsapk.co/300/f/6/f/com.appier.aiqua.demoapp.png",
            "image": "https://i.kinja-img.com/gawker-media/image/upload/s--PnSCSSFQ--/c_scale,f_auto,fl_progressive,pg_1,q_80,w_800/z7jcryloxjedsztssw39.jpg",
        },
        "views": {
            "v10": "l_0_0_100%_256_t_deeplink_o_tsbkgrnd_10",
            "v11": "r_2%_4_58_58_i_deeplink_o_isicon2_11",
            "v12": "l_2%_4_73%_21_t_deeplink_o_tstitle_12",
            "v13": "l_2%_24_73%_37_t_deeplink_o_tsmessage_13",
            "v14": "l_0_64_100%_192_i_deeplink_o_isimage_14",
            "v20":"l_0_0_100%_64_t_deeplink_o_tsbkgrnd_20"
        },
        "screens":["v10v11v13v12v14"],
        "cs":["v20v11v12v13"]
    }
    compressed_payload = get_compressed_string(dynamic_payload)
    # compressed_payload = 'H4sIAJGUuVwC_22SS2-jMBSF_wryqLs4fgAhzW7UVXeV2lmNqisehnhiHsImiabqf59rA5ooLbAw19-5PvfAB7GuIge-IefcTMqSwwfRZd-RAzk6N9gDY9om1Fqzbf9alztdbsu-ZbrNG8XccWoL9jKNg1FC7Nk5YalgWcpqiYssrSUvqIxVTKUo9jROREwfdzKLk3y3ryvFfg7DM55GORVX-MV5ptp8PCmnuwZr-5RKiVt8O3QNk8nuyi_bP0NDNsRpZxSafJqs69voZbLH6C3UNqRV1qI73H07ahvh45R10VKO6n6Mylk2oAwFYZibiS-Xy9bmLQ5Fz7pSvV1GbtjrXEUPNIhoyvmpWDxVSg1Gd6e7Tk3fN0b5Fv4o69OViEyjAb8G66BUnVPj09gPM7L4CYhff2GcXQNwVwdhDcaCgNyAUTWWSvjBwwVYTsHVUATd_3C8cnm7xbGN9Jp47eVlDvkgL07N2FXruQ4KFNbhIp_4D2l1Cb_QWXBkDHC8BecPINMdOFgTgh7WVriNjc9CID-CfIAE0r1_9C29xAaIeViG5gHOYmwu7nvPiSDn6Xil5YzH2T2-xoCoFySL910ymxeP8oud8FmQRF7ezYqy70dFEEOy5ahUhzH99jHh5OgQR_LHvm9IOW_IeUN69--f_wCUn7inpgMAAA=='
    users = []
    users.append({
        'gcmId': fcm_token
    })

    data = {
        'users': users,
        'title': 'some title',
        'message': 'some message',
        'type': 'basic',
        'dynamic': compressed_payload
    }

    success, response = send_push(fcm_key, data)
    print(success, response)
