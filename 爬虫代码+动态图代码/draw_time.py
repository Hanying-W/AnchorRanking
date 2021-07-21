# coding: utf-8
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from datetime import date, timedelta
import numpy as np
import csv
#解决显示中文字符的问题
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
df = pd.read_csv('douyu.csv',header=0,encoding='UTF-8',low_memory=False)
df.dropna(how='any')
time_sum =pd.date_range('2020-07-05 20:31:28', '2020-07-07 14:36:19', freq='1s')
#画好水平柱状图
fig, ax = plt.subplots(figsize=(15, 8))
list={}
def get_data(time):
    #ascending=True按照升序排序.sort_values(by='Live_viewer', ascending=True)
    dff = (df[df['time'].eq(time)])
    #print(dff['classification'][0])
    # print(str(dff ['Live_viewer']))
    with open('douyu.csv',encoding='UTF-8') as f:
        reader = csv.reader(f)
        flag=1
        for row in reader:
            if flag==1 :
                flag=flag-1
                continue
            s = str(row[4])
            if(s==('Live_viewer')):
                continue
            #s = s[s.find(' ') + 6:-1]
            #print(row[4])
            for i in dff['classification']:
                if i in list.keys():
                    list[i] += int(s)
                else:
                    list[i] = int(s)
                #print(list[i])
    print(sorted(list))
for i in time_sum:
    get_data(i)

