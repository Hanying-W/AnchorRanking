import requests
import time
import csv
import pandas as pd
import json
from bs4 import BeautifulSoup
from time import gmtime,strftime

def get_real_url(room_id):
    room_url = 'https://m.huya.com/' + str(room_id)#每个主播对应的ID
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
    #获得页面代码
    response = requests.get(room_url, headers=header).text
    #解析标签
    soup = BeautifulSoup(response, 'lxml')
    #找到对应的访问量标签，关注量
    all_content=soup.find_all('div', id='activityCount')
    #输出它的string类型
    num=all_content[0].string
    #print(all_content[0].string)
    #返回它的粉丝数
    return int(num)


#page, count, num, lis, game_list, hot_list = 1, 0, 1, {}, {}, {}
#定义CSV头部
headers=['序号','直播平台','直播类别','主播昵称','主播头像地址','实时观看人数','订阅者数量','时间']
#插入CSV文件
def huya_put_headers(headers):
    with open('huya.csv', 'a', encoding='utf-8-sig', newline='') as file:
        if (file==[]):
            file_csv = csv.writer(file)
            file_csv.writerow(headers)

#定义每一页
url = "https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&page="
def huya_get_list():
    page=1
    count=0;
    while True:
        # 进入每一页
        res = requests.get(url + str(page))
        # 设置一个字典存数据
        information = []
        # 将页面值转换为json格式
        response = res.json()
        # 获取每一个小窗口对应的值,具体值去网站查看对应含义
        artists = response['data']['datas']
        # 如果响应为空的话，代表遍历结束，数据分析打印
        if artists == None or artists == []:
            break;
        for i in artists:
            platform = '虎牙直播'
            nick = i['nick']  # //主播姓名
            nick_image_url = i['avatar180']  # 主播头像
            introduction = i['introduction']
            totalCount = i['totalCount']  # 主播人气
            gamename = i['gameFullName']  # 主播分类
            profileRoom = i['profileRoom']  # 主播的房间号
            # 总人气
            count += int(totalCount)
            # 日期时间
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            # 获取房间的粉丝量
            profileRoom = get_real_url(profileRoom)
            # 方便information的扩展
            temp_dict = [
                platform,
                gamename,
                nick,
                nick_image_url,
                totalCount,
                profileRoom,
                time
            ]
            information.append(temp_dict)
            page += 1
    return information

def huya_save_csv(information):
    #保存在csv文件中
    with open('huya.csv','a',encoding='utf-8-sig',newline='') as file:
        #标志我要写这个文件
        file_csv=csv.writer(file)
        #开始写
        file_csv.writerows(information)
#输入共爬取多少页
#返回index页的所有数据
def huya_get_list_now(index):
    page=1
    count=0;
    # 日期时间
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    # 设置一个字典存数据
    information = []
    while index:
        # 进入每一页
        res = requests.get(url + str(page))
        # 将页面值转换为json格式
        response = res.json()
        # 获取每一个小窗口对应的值,具体值去网站查看对应含义
        artists = response['data']['datas']
        # 如果响应为空的话，代表遍历结束，数据分析打印
        if artists == None or artists == []:
            break;
        for i in artists:
            Live_platform_name = '虎牙直播'
            nick = i['nick']  # //主播姓名
            nick_image_url = i['avatar180']  # 主播头像
            introduction = i['introduction']
            totalCount = i['totalCount']  # 主播人气
            gamename = i['gameFullName']  # 主播分类
            profileRoom = i['profileRoom']  # 主播的房间号
            introduction=i['introduction']#房间名字
            # 总人气
            count += int(totalCount)
            # 获取房间的粉丝量
            profileRoom = get_real_url(profileRoom)
            dizhi='https://m.huya.com/' + str(profileRoom)
            # 方便information的扩展
            temp_dict = [
                Live_platform_name,
                gamename,
                nick,
                nick_image_url,
                totalCount,
                profileRoom,
                time,
                dizhi,#直播地址
                introduction,#房间名字
            ]
            information.append(temp_dict)
        index -=1
        page += 1
    return information

list = huya_get_list_now(1)
print(list)