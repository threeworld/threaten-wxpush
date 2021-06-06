#! /usr/bin/python
# -*-coding:utf-8 -*-
# @Time     :   2021-03-12 16:10
# @Author   :   oneworld

from datetime import datetime

import requests
from requests.adapters import HTTPAdapter

from config import appToken, uids


class get_360_Threaten():
    
    def __init__(self, lasttime, time_path):
        self.url = 'https://cert.360.cn/warning/searchbypage'
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        self.lasttime = datetime.strptime(lasttime, '%Y-%m-%d %H:%M:%S')
        self.time_path = time_path
        self.getContent()
        
        
    def getContent(self, limit=6):
        
        req_session = requests.Session()
        req_session.mount('http://', HTTPAdapter(max_retries=3))
        req_session.mount('https://', HTTPAdapter(max_retries=3))

        param = {
            'length': limit,
            'start' : 0,
        }
        result = req_session.get(self.url, headers=self.headers, params=param, timeout=6)

        data = result.json()['data']
        
        for item in data:
            addTime = datetime.strptime(item.get('add_time_str') + ':00', '%Y-%m-%d %H:%M:%S')
            if addTime > self.lasttime:
                url = 'http://wxpusher.zjiecode.com/api/send/message'
                headers = {
                        'Content-Type': 'application/json; charset=UTF-8'
                    }
                data = {
                    "appToken" : appToken,                 # 填入自己申请的token
                    "content" : item.get('title') + "\n\n" + "摘要：" + item.get('description'),
                    "contentType" : 1,   
                    "uids" : uids,                      # 推送的用户id
                    "url": 'https://cert.360.cn/warning/detail?id=' + item.get('id')                  # 原文链接，可选参数 
                }
                try:
                    requests.post(url, headers=headers, json=data)
                except Exception as e:
                    print(e)
        nowtime = datetime.now()
        nowtime_str = nowtime.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.time_path, mode='r+') as f:
            f.write(nowtime_str)
        
if __name__ == '__main__':
    import os
    path = os.path.abspath(os.path.dirname(os.getcwd()))
    path = path + r'/time/cert360time.txt'
    with open(path, mode = 'r+') as f:
        lastime_str = f.readline()
    get_360_Threaten(lastime_str, path)
