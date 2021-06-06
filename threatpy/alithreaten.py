#! /usr/bin/python
# -*-coding:utf-8 -*-
# @Time     :   2021-03-11 16:51
# @Author   :   oneworld


from datetime import datetime

import requests
from lxml import etree
from requests.adapters import HTTPAdapter

from config import appToken, uids


class get_ali_Threaten():
    
    def __init__(self, lastime, time_path):
        self.url = 'https://help.aliyun.com/notice_list_page/9213612/1.html'
        self.lastime = datetime.strptime(lastime, "%Y-%m-%d %H:%M:%S")
        self.time_path = time_path
        self.vuls = self.getContent()
        
    def getContent(self):
        
        req_session = requests.Session()
        req_session.mount('http://', HTTPAdapter(max_retries=3))
        req_session.mount('https://', HTTPAdapter(max_retries=3))
        
        result = req_session.get(self.url, timeout=6)
        
        html = etree.HTML(result.text)
        
        vuls_name = html.xpath("//ul/li/a/text()")
        vuls_date = html.xpath("//ul/li/span[@class='y-right']/text()")
        vuls_time = html.xpath("//ul/li//span[@class='time']/text()")
        vuls_urlHref = html.xpath("//ul/li/a/@href")

        #拼接时间, URL
        for i in range(len(vuls_date)):
            addTime_str = vuls_date[i] + ' ' + vuls_time[i]
            addTime = datetime.strptime(addTime_str, "%Y-%m-%d %H:%M:%S")
            if addTime > self.lastime:
                
                url = 'http://wxpusher.zjiecode.com/api/send/message'
                headers = {
                        'Content-Type': 'application/json; charset=UTF-8'
                    }
                data = {
                    "appToken" : appToken,        
                    "content" : vuls_name[i] + "\n\n" + "时间: " + addTime_str,
                    "contentType" : 1,         #内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown 
                    "uids" : uids,              
                    "url": 'https://help.aliyun.com' + str(vuls_urlHref[i])   #原文链接，可选参数
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
    path = path + r'/time/alithreattime.txt'
    with open(path, mode = 'r+')  as f:
        lastime_str = f.readline().strip()
    get_ali_Threaten(lastime_str, path)
        

        
            
        
        
        
        
        
