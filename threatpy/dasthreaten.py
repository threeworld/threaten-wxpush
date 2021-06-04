#! /usr/bin/python
# -*-coding:utf-8 -*-
# @Time     :   2021-03-14 20:10
# @Author   :   oneworld

# 安恒威胁情报获取

from datetime import datetime

import requests
from lxml import etree
from requests.adapters import HTTPAdapter

from config import appToken, uids

#安恒威胁情报

class get_das_Threaten():
    
    def __init__(self, lastime, time_path):
        self.url = 'https://ti.dbappsecurity.com.cn/informationList'
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        }
        self.lastime = datetime.strptime(lastime, "%Y-%m-%d %H:%M:%S")
        self.time_path = time_path
        self.vuls = self.getContent()
        
    def getContent(self, limit=6):
        
        req_session = requests.Session()
        req_session.mount('http://', HTTPAdapter(max_retries=3))
        req_session.mount('https://', HTTPAdapter(max_retries=3))

        result = req_session.get(self.url, headers=self.headers, timeout=6)
        html = etree.HTML(result.text)
        #print(etree.tostring(html).decode())
        array = html.xpath("//ul[@class='infinite-list']//li")
        index = 0
        for item  in array:
            
            addTime_str = item.xpath(".//div[@class='list_info clearfix']//span[@class='time fl']/text()")[0]
            addTime = datetime.strptime(addTime_str, "%Y-%m-%d %H:%M:%S")
            if addTime > self.lastime:
                title = item.xpath(".//div[@class='list_title']//span/text()")[0]  
                content = item.xpath("//div[@class='list_str ']/@title")[index]
                index += 1
                url = 'http://wxpusher.zjiecode.com/api/send/message'
                headers = {
                        'Content-Type': 'application/json; charset=UTF-8'
                    }
                data = {
                    "appToken" : appToken,         # 填上自己申请的token
                    "content" : title + "\n\n" + "时间: " + addTime_str + "\n摘要: " + content,
                    "contentType" : 1,         #内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown 
                    "uids" : uids,              # 填上自己的wx id 
                    "url": self.url    #原文链接，可选参数
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
    path = r'./time/dasthreattime.txt'
    with open(path, mode = 'r+')  as f:
        lastime_str = f.readline().strip()
    get_das_Threaten(lastime_str, path)
