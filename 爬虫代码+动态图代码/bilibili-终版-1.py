from time import strftime

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import csv

from django.templatetags.tz import localtime

'''*****************************************************依据小分类进行爬取**********************************************'''


# 按照小类获取直播列表
def smallClassification():
    global information
    l = getSmallList()
    for i in l:
        sign = True
        page = 1
        while sign:
            # 构造申请链接
            url = 'https://api.live.bilibili.com/room/v3/area/getRoomList?' \
                  'platform=web&' \
                  'parent_area_id=' + i['parent_area_id'] + '&' \
                  'cate_id=0&' \
                  'area_id=' + i['area_id'] + '&' \
                  'sort_type=&' \
                  'page=' + str(page) + '&' \
                  'page_size=30&' \
                  'tag_version=1'

            # area_id 分类的编号
            # page 页码
            # page_size 每页显示的个数
            print(url)
            # 设置请求头
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/83.0.4103.116 Safari/537.36 '
            }
            # 发起请求
            html = requests.get(url, headers=headers)
            # 转换格式
            s = json.loads(html.text)
            # 设置存放数据的变量
            information = []
            # 解析数据
            for j in s['data']['list']:
                t = {
                    'Live_platform_name':'哔哩哔哩',
                    'roomid': j['roomid'],
                    'session_id': j['session_id'],
                    'roomName': j['title'],
                    'uid': j['uid'],
                    "Anchor_name": j['uname'],
                    'roomurl': "https://live.bilibili.com/{}?{}".format(j['roomid'], j['session_id']),
                    'classification': j['area_name'],
                    'Anchor_img': j['face'],
                    'time': strftime("%Y-%m-%d %H:%M:%S", localtime()),
                    
                }
                if not t:
                    sign = False
                    break
                information.append(t)
                try:
                    roomInfo = getLiveRoomInfo(t['roomurl'])
                except:
                    roomInfo = {
                        'Audience': 0,
                        'Live_Viewer': 0
                    }
                for k in roomInfo:
                    t[k] = roomInfo[k]
                print(t)
            page += 1
    with open('information.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(information))


# 获取主播直播间里面的一些信息
def getLiveRoomInfo(url):
    # 构造请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.116 Safari/537.36 '
    }
    # 发起请求
    html = requests.get(url, headers=headers)
    # 设置保存数据的变量
    returnData = {}
    # 转换格式
    s = BeautifulSoup(html.text)
    # 查找数据出现的地方
    pople = s.find_all('div', class_='script-requirement')
    # 提取数据
    t = pople[0].script.string
    t = t[t.find('WAIFU__') + 8:]
    # 转换格式方便保存
    js = json.loads(t)
    # 保存数据
    returnData['Audience'] = js['baseInfoRes']['data']['attention']
    returnData['Live_Viewer'] = js['baseInfoRes']['data']['online']
    # 返回获取到的数据
    return returnData


# 获取保存小类的信息
def getSmallList():
    with open('smallClassification.json', 'r', encoding='utf-8') as file:
        return json.loads(file.read())


'''****************************************依据大分类进行爬取***********************************************************'''


def bigClassification():
    l = getBigList()
    for i in l:
        sign = True
        page = 1
        while sign:
            url = 'https://api.live.bilibili.com/room/v3/area/getRoomList?' \
                  'platform=web&' \
                  'parent_area_id=' + i['parent_area_id'] + '&' \
                  'cate_id=0&' \
                  'area_id=0&' \
                  'sort_type=sort_type_' + i['sort_type'] + '&' \
                  'page=' + str(page) + '&' \
                  'page_size=30&' \
                  'tag_version=1'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/83.0.4143.116 Safari/537.36 '
            }
            html = requests.get(url, headers=headers)
            s = json.loads(html.text)
            print(s)
            print(url)
            information = []
            for j in s['data']['list']:
                t = {
                    'Live_platform_name':'哔哩哔哩',
                    'roomid': j['roomid'],
                    'session_id': j['session_id'],
                    'title': j['title'],
                    'uid': j['uid'],
                    'Anchor_name': j['uname'],
                    'roomurl': 'https://live.bilibili.com/{}?session_id={}'.format(j['roomid'], j['session_id']),
                    'classification': j['area_name'],
                    'Anchor_img': j['cover'],
                    'time': strftime("%Y-%m-%d %H:%M:%S", localtime()),
                    'roomName':j['title']
                }
                if not t:
                    sign = False
                    break
                print(t)
                information.append(t)

                try:
                    roomInfo = getLiveRoomInfo(t['roomurl'])
                except:
                    roomInfo = {
                        'Audience': 0,
                        'Live_Viewer': 0
                    }
                for k in roomInfo:
                    t[k] = roomInfo[k]
                print(t)
            with open('bili.csv', 'a', encoding='utf-8-sig', newline='') as file:
                file_csv = csv.writer(file)
                file_csv.writerows(information)
            page += 1


    # with open('information.json', 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(information))


def getBigList():
    with open('bigClassification.json', 'r', encoding='utf-8') as file:
        return json.loads(file.read())


'''*************************************************程序的入口*********************************************************'''
if __name__ == '__main__':
    # smallClassification()
    bigClassification()
    df = pd.read_csv('bili.csv')
    print(df)

    
    
