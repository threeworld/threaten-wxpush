from datetime import datetime

"""
初始化时间文件，把当前时间写进txt里
"""


alithreattime = '../time/alithreattime.txt'
cert360time = '../time/cert360time.txt'
dasthreatime = '../time/dasthreattime.txt'
txthreatime = '../time/txthreattime.txt'

now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(alithreattime, mode='r+') as f:
    f.write(now_time)

with open(cert360time, mode='r+') as f:
    f.write(now_time)
    
with open(dasthreatime, mode='r+') as f:
    f.write(now_time)
    
with open(txthreatime, mode='r+') as f:
    f.write(now_time)
