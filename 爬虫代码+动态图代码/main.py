import huya
import douyu
import cc
import qq

#获取每个平台的实时榜
#输入要获取的前几页
#返回各个平台前几页的记录
def get_rank(index):
    result=[]
    list = huya.huya_get_list_now(index)
    result.append(list)
    list = douyu.main_def(index)
    result.append(list)
    list = cc.get_data(index)
    result.append(list)
    list = qq.get_data(index)
    result.append(list)
    result = result.sort_values(by=5, ascending=True)
    return result

print(get_rank(1))