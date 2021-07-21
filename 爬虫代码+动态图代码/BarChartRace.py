# coding: utf-8
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from datetime import date, timedelta
df = pd.read_csv('data.csv',header=None)
#0 平台名字
#1 区域
#2 日期
#3 浏览量

#解决显示中文字符的问题
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

#改变颜色
#每个平台映射一个颜色
colors = dict(zip(['企鹅电竞','网易cc','龙珠','快手','yy','bilibili','斗鱼','虎牙'],
                  ['red','yellow','blue','green','black','grey','orange','purple']
                  ))
data=list(set(df[2]))
#print(data)

#画好水平柱状图
fig, ax = plt.subplots(figsize=(15, 8))
def draw_barchart(day):
    dff = (df[df[2].eq(day)].sort_values(by=3, ascending=True))
    #print(dff)
    ax.clear()#清除当前 figure 的所有axes，但是不关闭这个 window
    ax.barh(dff[0], dff[3], color=[colors[x] for x in dff[0]])
    # 宽度除以200
    dx = dff[3].max() / 200
    for i, (value, name) in enumerate(zip(dff[3], dff[0])):
        ax.text(value + dx, i, f'{value:,.0f}', size=14, ha='left', va='center')
    ax.text(1, 0.4, day,transform=ax.transAxes, size=46, ha='right', va='center')
def init():
    dff = (df[df[2].eq('2015-01-01')].sort_values(by=3, ascending=True))
    #print(dff)
    ax.clear()#清除当前 figure 的所有axes，但是不关闭这个 window
    ax.barh(dff[0], dff[3], color=[colors[x] for x in dff[0]])
    # 宽度除以200
    dx = dff[3].max() / 200
    for i, (value, name) in enumerate(zip(dff[3], dff[0])):
        ax.text(value + dx, i, f'{value:,.0f}', size=14, ha='left', va='center')
#遍历日期
date=pd.date_range('2015-01-01', '2020-07-01', freq='D')

ani = animation.FuncAnimation(fig=fig,
func=draw_barchart,
frames=date.strftime("%Y-%m-%d",
init_func=init,#动画最初是啥样的
interval=20,#更新频率 20ms
blit=False,#更新部分图片，变化了就更新，False如果变化了就全部数据更新
 )
plt.show()
