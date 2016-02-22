# coding:utf8
__author__ = 'yuan.gao'
import urllib, urllib2
import json, time
from urllib2 import URLError


class DingDing:
    def __init__(self):
        self.url = 'https://oapi.dingtalk.com/gettoken?corpid=ding7dd0fd2e5b257e6e&corpsecret=9QzGezdj8HDwNLrZDE2Bx2dq6ckrN1rsvH0hDtuUPcuEYi_65P6HIS9hEZNN1zxb'
        self.header = {"Content-Type":"application/json"}
        self.authID = self.get_token()

    def get_token(self):
        request = urllib2.Request(self.url)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "\033[041m 出错:\033[0m", e
        else:
            response = json.loads(result.read())
            result.close()
#            self.authID = response['result']
            authID = response['access_token']
            return authID

    def send_link_message(self, ddID, json_content):
        # message = '[%s]\n%s' % (time.strftime('%Y%m%d %H:%M:%S'))
        data = {
            "touser":ddID,
            "agentid":"4162046",
            "msgtype":"link",
            "link":json_content
        }
        print data
        requrl = 'https://oapi.dingtalk.com/message/send?access_token=' + self.authID
        quoteUrl=urllib.quote_plus(requrl, safe=':\'/?&=()')
        postData = json.dumps(data)
        req = urllib2.Request(url=quoteUrl, data=postData)
        req.add_header('Content-type', 'application/json')
        try:
            res_data = urllib2.urlopen(req)
        except URLError as e:
            print "\033[041m 出错:\033[0m", e
        else:
            res = res_data.read()
#       print res

if __name__ == "__main__":
    dd = DingDing()
    jsonmsg = {
        "title": "asd",
        "text": "asdsdads",
        "picUrl": "@lALOACZwe2Rk",
        "messageUrl": "http://s.dingtalk.com/market/dingtalk/error_code.php",
    }
    dd.send_link_message(ddID='yuan.gao', json_content=jsonmsg)