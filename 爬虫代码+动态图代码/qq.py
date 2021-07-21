import requests
from bs4 import BeautifulSoup
from time import localtime, strftime, sleep
import csv

# User-Agent
ua = {'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}


def get_url(index):
    return 'https://share.egame.qq.com/cgi-bin/pgg_async_fcgi?param=%7B%22key%22:%7B%22module%22:%22pgg_live_read_ifc_mt_svr%22,%22method%22:%22get_pc_live_list%22,%22param%22:%7B%22appid%22:%22hot%22,%22page_num%22:' + str(
        index) + ',%22page_size%22:40,%22tag_id%22:0,%22tag_id_str%22:%22%22%7D%7D%7D&app_info=%7B%22platform%22:4,%22terminal_type%22:2,%22egame_id%22:%22egame_official%22,%22imei%22:%22%22,%22version_code%22:%229.9.9.9%22,%22version_name%22:%229.9.9.9%22,%22ext_info%22:%7B%22_qedj_t%22:%22%22,%22ALG-flag_type%22:%22%22,%22ALG-flag_pos%22:%22%22%7D,%22pvid%22:%22853146214420070817%22%7D&g_tk=&pgg_tk=&tt=1&_t='


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
    for i in range(len(json_text['data']['key']['retBody']['data']['live_data']['live_list'])):
        data_list = json_text['data']['key']['retBody']['data']['live_data']['live_list'][i]
        temp_dict = [
            '企鹅电竞',
            data_list['appname'],  # 所在分类名称
            data_list['anchor_name'],  # 主播名字
            data_list['anchor_face_url'],  # 主播头像
            data_list['fans_count'],  # 粉丝人数
            data_list['online'],  # 实时观看人数
            time,  # 时间
            data_list['jump_url'],#主播链接
            data_list['title'],  # 直播间名字
        ]
        qq_list.append(temp_dict)
    return qq_list


def get_data(index):
    result = []
    # 获取当前时间
    time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    for i in range(1, index):
        url = get_url(i)
        json_text = page_def(url, ua)
        qq_list = info_def(json_text, time)
        result.append(qq_list)
    return result

def put_csv(qq_list):
    with open(r'qq.csv', 'a', encoding='utf-8-sig', newline='') as cf:
        file_csv = csv.writer(cf)
        file_csv.writerows(qq_list)