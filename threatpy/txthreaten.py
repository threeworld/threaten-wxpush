#! /usr/bin/python
# -*-coding:utf-8 -*-
# @Time     :   2021-03-11 16:51
# @Author   :   oneworld


from datetime import datetime

import requests
from requests.adapters import HTTPAdapter

from config import appToken, uids


class get_tx_Threaten():
    
    def __init__(self, lastime, time_path):
        self.url = "https://cloud.tencent.com/announce/ajax"
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        self.lastime = datetime.strptime(lastime, "%Y-%m-%d %H:%M:%S")
        self.time_path = time_path
        self.count = self.getCount()
        self.getContent()
        
    def getCount(self):
        params = {
            "action": "getAnnounceList",
            "data": 
                {"rp": 1, 
                 "page": "1", 
                 "categorys": ["21"], 
                 "labs": [], 
                 "keyword": "",
                 }
        }
        #超时重试
        req_session = requests.Session()
        req_session.mount('http://', HTTPAdapter(max_retries=3))
        req_session.mount('https://', HTTPAdapter(max_retries=3))
        
        try:
            result = requests.post(self.url, headers=self.headers, json=params, timeout=5)
            return result.json()['data']['total']
        except requests.exceptions.RequestException as e:
            print(e)
        
        
    def getContent(self):
        params = {
            "action": "getAnnounceList",
            "data": 
                {"rp": self.count, 
                 "page": "1", 
                 "categorys": ["21"], 
                 "labs": [], 
                 "keyword": "",
                 }
        }
        #超时重试
        req_session = requests.Session()
        req_session.mount('http://', HTTPAdapter(max_retries=3))
        req_session.mount('https://', HTTPAdapter(max_retries=3))
        try:
            result = requests.post(self.url, headers=self.headers, json=params, timeout=5)
            rows = result.json()['data']['rows']
        except requests.exceptions.RequestException as e:
            print(e)
        
        for row in rows:
            addTime = datetime.strptime(row.get('addTime'), "%Y-%m-%d %H:%M:%S")
            if addTime > self.lastime:
                
                url = 'http://wxpusher.zjiecode.com/api/send/message'
                headers = {
                        'Content-Type': 'application/json; charset=UTF-8'
                    }
                data = {
                    "appToken" : appToken,         # 填上自己申请的token
                    "content" : row.get('title') + "\n\n" + "时间: " + row.get('addTime'),
                    "contentType" : 1,         #内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown 
                    "uids" : uids,              # 填上自己的wx id 
                    "url": 'https://cloud.tencent.com/announce/detail/' + row.get('announceId')   #原文链接，可选参数
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
    
    path = r'./time/txthreattime.txt'
    with open(path, mode = 'r+')  as f:
        lastime_str = f.readline().strip()
    get_tx_Threaten(lastime_str, path)
        
