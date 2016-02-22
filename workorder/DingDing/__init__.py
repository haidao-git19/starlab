# coding:utf8
__author__ = 'yuan.gao'
import requests
import json


class DingDing:
    def __init__(self):
        #
        self.url = 'https://oapi.dingtalk.com/gettoken?corpid=ding7dd0fd2e5b257e6e&corpsecret=9QzGezdj8HDwNLrZDE2Bx2dq6ckrN1rsvH0hDtuUPcuEYi_65P6HIS9hEZNN1zxb'
        self.header = {"Content-Type":"application/json"}
        # 获取cookie
        r = requests.get(self.url)
        if r.status_code == 200:
            if r.json()['access_token']:
                self.access_token = r.json()['access_token']
            else:
                raise Exception('Error from source %s' % r.text)
        else:
            raise Exception('Error from source %s' % r.text)

    def send_link_message(self, ddID, json_content):
        """
        :param ddID: 用户ID号,格式为UserID1|UserID2|UserID3
        :param json_content: 字典,4个值,缺一不可
            例如:
            {
                "title": "审批加签",
                "text": "你被加签到一个变更审批:{}\n任务ID:{}".format(task.itemId.itemName, task.id),
                "picUrl": "@lALOACZwe2Rk",
                "messageUrl": url,
            }
        :return:
            成功:
            {
                "errcode":0,
                "errmsg":"ok",
                "invalidparty":"",
                "invaliduser":""
            }
        """
        data = {
            "touser":ddID,
            "agentid":"4162046",
            "msgtype":"link",
            "link":json_content
        }
        url = 'https://oapi.dingtalk.com/message/send?access_token=' + self.access_token
        data = json.dumps(data)
        r = requests.post(url, data=data, headers={'content-type': 'application/json'})
        print r.text


if __name__ == "__main__":
    dd = DingDing()
    data = {
        "title": "审批加签",
        "text": "test",
        "picUrl": "@lALOACZwe2Rk",
        "messageUrl": 'https://www.baidu.com',
    }
    dd.send_link_message(ddID='yuan.gao|zilu.yb', json_content=data)