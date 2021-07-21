import requests
from bs4 import BeautifulSoup
from time import localtime,strftime,sleep
import csv

#请求网页
def page_def(url,ua):
    # 获得页面HTML;
    resp = requests.get(url,headers = ua)
    # 获取json文件
    json_text = resp.json()
    return json_text


#解析网页
def info_def(json_text,time):
    douyu_list=[]
    #time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    for i in range(len(json_text['data']['rl'])):
        data_list = json_text['data']['rl'][i]
        #print(data_list)
        #每条记录的数据
        temp_dict=[
            '斗鱼',
            data_list['c2name'], #分类
            data_list['nn'], #昵称
            data_list['rs1'],#头像
            '',#订阅者数量
            data_list['ol'], #实时观看人数
            time,#时间
            'https://www.douyu.com/' + str(data_list['rid']),  # 链接，主播直播连接
            '',#房间名字
        ]
        douyu_list.append(temp_dict)
    return douyu_list

#写入csv
def csv_def(douyu_list):
    with open(r'douyu.csv','a',encoding='utf-8-sig',newline='') as cf:
        file_csv=csv.writer(cf)
        file_csv.writerows(douyu_list)         
    #print("一页爬取完成！")

#主函数
def main_def(index):
    #文件的头
    headers= ['Live_platform_name','classification','Anthor_name','url','Live_viewer','time','Anchor_img']
    with open(r'douyu.csv','a',encoding='utf-8-sig',newline='') as cf:
        file_csv=csv.writer(cf)
        #print('3254432543')
        file_csv.writerow(headers)
        #w = csv.DictWriter(cf,fieldnames =)
    result=[]
    # User-Agent
    ua = {'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
    #获取当前时间
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    #获取index个页面的代码
    for i in range(1,index):
        #每个页面的地址
        url = 'https://www.douyu.com/gapi/rkc/directory/mixList/0_0/%d'%(i)
        #获得代码
        json_text = page_def(url,ua)
        # 返回代码中的我们需要的值
        douyu_list = info_def(json_text,time)
        result.append(douyu_list)
        #print("正在爬取第%d"%(i)+"页")
        csv_def(douyu_list)
    return result

