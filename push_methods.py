import urllib, urllib2
import json
def qpush_send(user, msg):
    url = "https://qpush.me/pusher/push_site/"
    headers = {
        'Host': 'qpush.me',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://qpush.me',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://qpush.me/en/push/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
    }
    data = {
        'name' : user.credentials['device_name'],
        'code' : user.credentials['device_pushcode'],
        'sig' : '',
        'cache' : 'false',
        'msg[text]' : msg
        }

    request = urllib2.Request(url, data=urllib.urlencode(data), headers=headers)
    response = urllib2.urlopen(request)

def pushbullet_send(user, msg):
    print "Pushbullet"
    print "Send to :" + user.name
    print "msg : {" + msg + "}"
    url = 'https://api.pushbullet.com/v2/pushes'

    header = {
        'Access-Token': user.credentials["access_token"], 
        'Content-Type':'application/json'
    }

    data = {
        "body": msg, 
        "title": "[General Indicator Notification]", 
        "type":"note"
    }
    data= json.dumps(data)
    print type(data), data
    req = urllib2.Request(url, data=data, headers=header)
    response = urllib2.urlopen(req)
    print response    


SEND_METHOD = {"qpush":qpush_send, "pushbullet":pushbullet_send}
