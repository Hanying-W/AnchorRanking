from wordcloud import WordCloud, ImageColorGenerator
from imageio import imread
import jieba

stopWords = ['一个', '看着', '很多', '应该', '我们', '仿佛', '看到', '就是', '此时', '还是', '只是', '什么', '如果', '开始', '现在', '依然', '可能', '知道',
             '那些', '因为', '然后', '自己', '他们', '所以', '然而', '没有', '那么', '这些', '便是', '那个', '不是', '没有', '虽然', '自然', '已经']

mask = imread('D:\\课件\\python\\final\\images.png')

with open('name.txt', 'r', encoding='utf-8') as f:
    txt = f.read()

# color = wordcloud.ImageColorGenerator(image,default_color = (0,0,255))

txt_list = jieba.lcut(txt)
txt_list = [w for w in txt_list if w not in stopWords]
txt = ' '.join(txt_list)

wd = WordCloud(
    font_path='C:\\WINDOWS\\FONTS\\MSYH.TTC',#
    width=800,
    height=400,
    max_words=2000,
    max_font_size=40,
    margin=2,
    ranks_only=False,
    prefer_horizontal=1.1,
    scale=1,
    background_color='white',
    mask=mask,
    mode="RGBA",
    include_numbers=True
)

wd.generate(txt)
# wd.recolor(color_func=color)
wd.to_file('D:\\课件\\python\\final\\mine.png')

