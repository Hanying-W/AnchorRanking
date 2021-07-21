import json
import requests
from bs4 import BeautifulSoup

# 获取分类
def getClassificationList():
    
    url = 'http://starapicdn.longzhu.com/roomtag/getsidebar?lzv=undefined'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    
    t = json.loads(requests.get(url, headers=headers).text)
    
    information = []
    
    for i in t['mainCategory']:
        for j in i['list']:
            t = {
                'classification':j['categoryTitle'],
                'classificationUrl' :j['jumpUrl']
            }
#             print(t)
            information.append(t)
    
    with open('classification.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(information))
        
def getRoomInfo(url):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    
    html = requests.get(url, headers=headers, allow_redirects=False).text
    
    s = BeautifulSoup(html, 'html')
    
    t = json.loads(html[html.find('var roomHost') + 15:html.find('var roomGrade') - 10])
    
    returnData = {
        'Anchor_name':t['username'],
        'Audience':getUserInfo(t['uid'])
    }
    
    return returnData
    
    
def getLiveViewer(roomId):
    
    url = 'http://roomapicdn.longzhu.com/room/roomstatus?' \
    'roomid=' + str(roomId) + '&' \
    'lzv=1'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    
    html = requests.get(url, headers=headers, allow_redirects=False).text
    
    t = json.loads(html)
    
    return t['OnlineCount']
   
def getUserInfo(toUserID):

    url = 'http://mservice.longzhu.com/relationship/stat?' \
    'toUserID=' + str(toUserID) + '&' \
    'lzv=undefined'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    
    html = requests.get(url, headers=headers).text
    
    t = json.loads(html)
    
    return t['fansCount']




# 获取当前直播列表
def getLiveList(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    
    html = requests.get(url, headers=headers)
    
    t = BeautifulSoup(html.text, 'html')
    
    information = []
    
    s = t.find_all('div', class_='list-con')
    
    if len(s) == 0:
        return
    
    s = s[0].find_all('a')
    
    for i in s:
#         print(i)
        s = i['data-label']
        roomid = s[s.find('roomid') + 7:s.find('domain') - 1]
        t = {
            'Live_platform_name':'虎牙',
            'classification':i.ul.find_all('li')[1].find_all('span')[1].string,
            'roomUrl':'https:' + i['href'],
            'Anchor_img':i.img['src'],
            'roomName':i.img['alt'],
            'Live_viewer':getLiveViewer(roomid)
        }
        s = getRoomInfo(t['roomUrl'])
        for i in s:
            t[i]=s[i]
        print(t)
        information.append(t)
        
    fileName = url[url.find('channels/') + 9:]
    
    with open(fileName, 'w', encoding='utf-8') as file:
        file.write(json.dumps(information))
    
if __name__ == '__main__':
    getClassificationList()
    with open('classification.json', 'r', encoding='utf-8') as file:
        information = json.loads(file.read())
    for i in information:
        print(i['classificationUrl'])
        getLiveList(i['classificationUrl'])
        
