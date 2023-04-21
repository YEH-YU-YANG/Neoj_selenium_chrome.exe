import time
import requests
import json
from fake_useragent import UserAgent
import random

challenge_list_url = 'https://neoj.sprout.tw/api/challenge/list'

### Database 
user_list = [3856,4028,4001,3999,3853,3964,3236,3893,3848,3880,4026,3965,3996,3994,3855,4029,3849,3867,3874,3962,3881,3981,4008,4018,3997,3986,4009,3899,3883,3995,3234,3974,3847,4106,3872,3892,3862,4019,3851,3854,3879,3976,3985,3958,3959,3852,4027,3980,
             3978,4030,3871,3998,3967,3465,3864,3897,4070,3957,4007,3972,3979,3876,3877,3861,3859,4010,4006,3898,3993,3984,3884,4016,3878,3887,3860,4002]

problem_list = {
    'deadline' : '20230311',
    'pid' : [288]
}
###

def getEarliestAC(uid, pid, deadline):

    payload = '{"offset":0,"filter":{"user_uid":"%s","problem_uid":"%s","result":"1"},"reverse":true,"chal_uid_base":null}' % (uid, pid)
    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'user-agent' : UserAgent().random,
        'Referer': 'https://neoj.sprout.tw/status/',
    }

    status = json.loads(requests.post(challenge_list_url, payload,headers=header).text)
    
    # info: 學生的第一筆AC資料 , 以json格式串給driver 
    info = {
        'ac_time':'',
        'challenge': '',
        'student_id': uid,
        'problem_id': pid,
        'start_day' : int(deadline)-7
    }    
    
    if status['count'] == 0:
        info['challenge'] = 'null'
        info['ac_time'] = 1e9
        return info
    
    date = int(status['data'][0]['timestamp'][:10].replace('-', ''))
    if int(status['data'][0]['timestamp'][11:13]) >= 16:
        date += 1
        
    info['challenge'] = status['data'][0]['uid']
    info['ac_time'] = date
    return info


#### main ####

#### 隨機停留秒數，避免被網站當爬蟲而被抵擋
delay_choices = [1, 3, 5]  #延遲的秒數
delay = random.choice(delay_choices)  #隨機選取秒數

#### 串給drive的list
info_list=[]

#### 
for pid in problem_list['pid']:
    for uid in user_list:
        # time.sleep(delay)  #延遲 , 怕被網站擋就設定延遲
        info = getEarliestAC(uid,pid,problem_list['deadline'])
        if info['ac_time'] <= (int(problem_list['deadline'])) :
            info_list.append(info)  
        print(info)

# for obj in info_list:
#     print(obj)
        
