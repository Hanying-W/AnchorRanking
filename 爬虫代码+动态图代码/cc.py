import requests
from bs4 import BeautifulSoup
from time import localtime, strftime, sleep
import csv

# User-Agent
ua = {'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}


def get_url(index):
    return 'https://cc.163.com/api/category/live/?format=json&start=' + str(
        index) + '&size=30'


# 请求网页
def page_def(url, ua):
    # 获得页面HTML;
    resp = requests.get(url, headers=ua)
    # 获取json文件
    json_text = resp.json()
    return json_text


# 解析网页
def info_def(json_text, time):
    qq_list = []
    for i in range(len(json_text['lives'])):
        data_list = json_text['lives'][i]
        temp_dict = [
            '网易cc',
            data_list['gamename'],  # 所在分类名称
            data_list['nickname'],  # 主播名字
            data_list['purl'],  # 主播头像
            data_list['follower_num'],  # 粉丝人数
            data_list['hot_score'],  # 实时观看人数
            time,  # 时间
            '',#直播间链接
            data_list['title'],  # 直播间名字
        ]
        qq_list.append(temp_dict)
    return qq_list


def get_data(index):
    # 获取当前时间
    result=[]
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    for i in range(1, index):
        url = get_url( i*30 )
        json_text = page_def(url, ua)
        qq_list = info_def(json_text, time)
        with open(r'cc.csv', 'a', encoding='utf-8-sig', newline='') as cf:
            file_csv = csv.writer(cf)
            file_csv.writerows(qq_list)
        result.append(qq_list)



get_data(80)