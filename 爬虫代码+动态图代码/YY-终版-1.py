import requests
import json
from bs4 import BeautifulSoup


def getClassificationList():
    
    url = 'https://www.yy.com/catalog'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

    html = requests.get(url, headers=headers).text
    
    s = BeautifulSoup(html, 'html')
    
    information = []
    
    for i in s.find_all('ul')[4].find_all('li'):
#         print(i, end='\n\n\n')
        t = {
            'classification':i.a.find_all('span')[2].string,
            'classificationUrl':'https://www.yy.com' + i.a['href']
        }
        if '直播购' in t['classification']:
            continue
        if '神曲' in t['classification']:
            continue
        if '小视频' in t['classification']:
            continue
        print(t)
        information.append(t)
    with open('YYClassification.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(information))
    

# 获取直播列表
def getRoomList(url):
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    
    html = requests.get(url).text
    
    s = BeautifulSoup(html, 'html')
    
    pageInfo = html[html.find('pageBar') + 10:]
    
    pageInfo = pageInfo[:pageInfo.find('position') - 19]
    
    pageInfo = '{' + pageInfo + '}'
    
    print(pageInfo)
    
    nextPage(pageInfo)
    
# 在房间里面获取关注人数
def getRoomInfo(url):
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    html = requests.get(url, headers=headers).text
    s = html[html.find('pageInfo'):]
    s = s[:s.find('flashUrlPrefix')]
    s = s[s.find('owInfo'):]
    return s[s.find('numOfFun') + 11:s.find('title') - 19]

def nextPage(pageInfo):
    
    biz = pageInfo[pageInfo.find('biz') + 5:pageInfo.find('subBiz') - 3]
    
    subBiz = pageInfo[pageInfo.find('subBiz') + 8:pageInfo.find('showImpress') - 3]
    
    pageSize = pageInfo[pageInfo.find('pageSize') + 9:pageInfo.find('moduleId') - 2]
    
    moduleId = pageInfo[pageInfo.find('moduleId') + 9:pageInfo.find('biz') - 2]
    
    for i in range(1, int(pageSize)):
        
        url = 'https://www.yy.com/more/page.action?' \
        'biz=' + biz + '&' \
        'subBiz=' + subBiz + '&' \
        'page=' + str(i) + '&' \
        'moduleId=' + moduleId + '&' \
        'pageSize=60'

        print(url)
        
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        
        html = requests.get(url, headers=headers).text
        subBiz = 'cjzc'
        for i in json.loads(html)['data']['data']:
            t = {
                'Live_platform_name':'YY直播',
                'classification':subBiz,
                'Anchor_name':i['name'],
                'Anchor_img':i['avatar'],
                'Audience':getRoomInfo('https://www.yy.com/' + i['liveUrl']),
                'Live_viewer':i['users'],
                'rooomUrl':'https://www.yy.com/' + i['liveUrl'],
                'roomName':i['desc']
            }
            print(t)
    
if __name__ == '__main__':
    getClassificationList()
    
    with open("YYClassification.json", 'r', encoding='utf-8') as file:
        l = json.loads(file.read())
        for i in l:
            getRoomList(i['classificationUrl'])
