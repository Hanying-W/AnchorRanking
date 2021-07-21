import json
import queue
import math
import datetime
import time
import random

import requests

PROVINCE_CODE = {'山东': '901', '贵州': '902', '江西': '903', '重庆': '904', '内蒙古': '905', '湖北': '906', '辽宁': '907',
                 '湖南': '908', '福建': '909', '上海': '910', '北京': '911', '广西': '912', '广东': '913', '四川': '914',
                 '云南': '915', '江苏': '916', '浙江': '917', '青海': '918', '宁夏': '919', '河北': '920', '黑龙江': '921',
                 '吉林': '922', '天津': '923', '陕西': '924', '甘肃': '925', '新疆': '926', '河南': '927', '安徽': '928',
                 '山西': '929', '海南': '930', '台湾': '931', '西藏': '932', '香港': '933', '澳门': '934'}


class BaiduIndex:
    headers = {
        'Cookie': 'bdshare_firstime=1584153505038; PSTM=1587717926; BAIDUID=61C0DD361DBE8854428A554C924F79F3:FG=1; BIDUPSID=2EA81B3E682FE0EDFA3A5F964E8669B5; BDUSS=0N1TVlnUXBoNmdZRlpmeHQ3Skd5YWh6WUkyS0N5M0VVc1ZITmNJMmNJS0JMTlJlSVFBQUFBJCQAAAAAAAAAAAEAAAAkRq8GNDA3NDg4MDE5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIGfrF6Bn6xed; MCITY=-257%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; yjs_js_security_passport=28d252da92a78fb4c9add210a7e88880774e3c4e_1589542914_js; H_PS_PSSID=1443_31326_21101_31254_31591_31463_31228_30823_26350_22157; delPer=0; PSINO=6; BCLID=9209142316339314792; BDSFRCVID=JLkOJeC62AfsIhTulvOehfuA8dhDnMTTH6aIajvXYoPQTaDQvO9TEG0PoM8g0Kub7B9ZogKK3gOTH4DF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tJK8VIL2JC_3fP36q4jHhRD0-fTeK4uXKKOLVhc12h7keq8CDxQtKUFJ3hoQ-fR-2Ict5Cne2pb_8fb2y5jHyt_q5R7k2hOIQI6Rb4QvfxbpsIJMhUFWbT8U5fKf3jczaKviaKOjBMb1MhbDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe4tX-NFDt6-qtU5; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1589620196; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1589620196; bdindexid=vebjcconrc111858bb88orsuq3; RT="z=1&dm=baidu.com&si=107oibszyipa&ss=ka9etknw&sl=2&tt=1h4&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1vf&ul=2o5s"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    kind = 'all'  # all, pc, wise
    params_queue = queue.Queue()
    days = 300  # 时间区间，每次请求300天的数据

    def __init__(self, keywords: list, start_date: str, end_date: str, areas=[]):
        self.keywords = keywords
        self.areas = {'全国': 0}
        self.init_params_queue(keywords, start_date, end_date, areas)

    # 初始化地区
    def init_area(self, areas):
        if areas:
            obj = {}
            for ares in areas:
                if code == PROVINCE_CODE.get(ares):
                    obj[ares] = code
            self.areas = obj
        return self.areas

    # 初始化请求队列
    def init_params_queue(self, keywords, start_date, end_date, areas):
        areas = self.init_area(areas)
        keyword_list = self.split_words(keywords)
        time_list = self.get_time_list(start_date, end_date)
        for keywords_group in keyword_list:
            for area_name, area_code in areas.items():
                for start_date, end_date in time_list:
                    obj = {
                        'area_name': area_name,
                        'params': {
                            'word': json.dumps(keywords_group, ensure_ascii=False),
                            'area': area_code,
                            'startDate': start_date.strftime('%Y-%m-%d'),
                            'endDate': end_date.strftime('%Y-%m-%d')
                        }
                    }
                    self.params_queue.put(obj)

    # 切分关键词，百度最多一次请求5个词组
    def split_words(self, keywords):
        keywords_list = []
        for i in range(math.ceil(len(keywords) / 5)):
            group = keywords[i * 5: (i + 1) * 5]
            new_group = []
            for word in group:
                obj = {
                    "name": word,
                    "wordType": 1
                }
                new_group.append([obj])
            keywords_list.append(new_group)

        return keywords_list

    # 时间分组
    def get_time_list(self, start_date, end_date):
        time_list = []
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        while 1:
            temp_date = start_date + datetime.timedelta(days=300)
            if temp_date > end_date:
                time_list.append((start_date, end_date))
                break
            time_list.append((start_date, temp_date))
            start_date = temp_date + datetime.timedelta(days=1)
        return time_list

    # 请求百度指数获得数据
    def request_data(self, params):
        url = 'http://index.baidu.com/api/SearchApi/index'
        res = requests.get(url, headers=self.headers, params=params, timeout=5)
        if res.status_code != 200:
            raise requests.Timeout
        datas = json.loads(res.text)
        if not datas['data']:
            return print('接口返回数据异常：', datas)
        userIndexes = datas['data']['userIndexes']
        uniqid = datas['data']['uniqid']
        return userIndexes, uniqid

    # 根据 uniqid 获得 密钥
    def get_key(self, uniqid):
        url = 'http://index.baidu.com/Interface/ptbk?uniqid=' + uniqid
        res = requests.get(url, headers=self.headers)
        datas = json.loads(res.text)
        key = datas['data']
        return key

    # 数据解密
    def decrypt(self, key, data):
        a = key
        i = data
        n = {}
        s = []
        for o in range(len(a) // 2):
            n[a[o]] = a[len(a) // 2 + o]
        for r in range(len(data)):
            s.append(n[i[r]])
        return ''.join(s).split(',')

    def format_data(self, data, area_name):
        word = str(data['word'][0]['name'])
        time_length = len(data[self.kind]['data'])
        start_date = data[self.kind]['startDate']
        cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        for i in range(time_length):
            index_datas = data[self.kind]['data']
            index_data = index_datas[i]
            formated_data = {
                'word': word,
                'type': area_name,
                'date': cur_date.strftime('%Y-%m-%d'),
                'index': index_data if index_data else '0'
            }
            yield formated_data
            cur_date += datetime.timedelta(days=1)

    def get_index(self):
        fd = open(f'./data.csv', mode='w', encoding='utf-8')
        while True:
            try:
                param_item = self.params_queue.get(timeout=1)
                print(param_item)
                userIndexes, uniqid = self.request_data(param_item['params'])
                key = self.get_key(uniqid)
                for data_item in userIndexes:
                    data = data_item[self.kind]['data']
                    # 这里对返回的data判断一下，有可能当前时间段数据为空，如果为空则手动填充为0
                    if data:
                        data_item[self.kind]['data'] = self.decrypt(key, data)
                    else:
                        data_item[self.kind]['data'] = [0] * (self.days + 1)
                    for item in self.format_data(data_item, param_item['area_name']):
                        line = ','.join(item.values())
                        print(line)
                        fd.write(line)
                        fd.write('\n')
            except requests.Timeout:
                self.params_queue.put(param_item)
            except queue.Empty:
                break
            time.sleep(random.randint(1, 3))


if __name__ == '__main__':
    # areas = ['广东', '上海']  # 默认不填就是全国
    # areas = [i for i in PROVINCE_CODE]  # 所有省份
    areas = []  # 全国
    keywords = ['Bilibili', 'YY', '斗鱼', '快手', '网易CC', '企鹅电竞', '龙珠', '虎牙']
    start_date = '2015-01-01'
    end_date = '2020-07-01'
    keywords = list(set([k.strip() for k in keywords]))  # 去重
    spider = BaiduIndex(keywords, start_date, end_date, areas)
    spider.get_index()
