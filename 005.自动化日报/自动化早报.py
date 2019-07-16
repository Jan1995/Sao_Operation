# 首发于微信公众号：小詹学Python
# 个人微信号：xiaozhan_god
import re
import time
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

# 获取第一个早报的url
obj1 = requests.get('http://www.pmtown.com/archives/category/早报')
url_obj = BeautifulSoup(obj1.text, 'lxml')
url = url_obj.find('h2').find('a').get('href')
first_url = 'http://www.pmtown.com' + url


# 获取当前页的东西
obj = requests.get(first_url)
obj_1 = BeautifulSoup(obj.text, 'lxml')
titles = obj_1.findAll('p')

# 获得日报文本
a = []
for title in titles:
    a.append(title.get_text())


# 判断融资收购、国内动态和海外动态位置
i = 0
for i in range(len(a)):
    if "【国内动态】" in a[i]:
        gn = i
    elif "【海外动态】"in a[i]:
        hw = i
    elif "【融资收购】"in a[i]:
        rz = i
    else:
        i = i + 1
print(gn, hw, rz)


# 讲新闻文本格式统一，生成新的列表
def get_text(text_orgin):
    first_list = re.sub(r'\d{1,2}、', 'SP', text_orgin)
    mid_list = first_list.split('SP')
    finnal_list = mid_list[1:len(mid_list)]
    return finnal_list


# 开始画图
header = '互联网日报'
title = '由python脚本自动生成'


# 图片名称
img = './daily.jpeg'  # 图片模板
new_img = 'daily1.jpeg'  # 生成的图片
compress_img = 'daily2.jpeg'  # 压缩后的图片


# 设置字体样式
font_type = 'C:/Windows/Fonts/simkai.ttf'
font_medium_type = 'C:/Windows/Fonts/simkai.ttf'
header_font = ImageFont.truetype(font_medium_type, 55)
title_font = ImageFont.truetype(font_medium_type, 20)
font = ImageFont.truetype(font_type, 38)
color = "#726053"
color1 = "#294E76"

# 打开图片
image = Image.open(img)
draw = ImageDraw.Draw(image)
width, height = image.size
print(width, height)

# header头
header_x = 130
header_y = 200
draw.text((header_x, header_y), u'%s' % header, color, header_font)

# 标题
title_x = header_x
title_y = header_y + 80
draw.text((title_x, title_y), u'%s' % title, color1, title_font)

# 当前时间
cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
cur_time_x = 666
cur_time_y = title_y
cur_time_font = ImageFont.truetype(font_type, 20)
draw.text((cur_time_x, cur_time_y), u'%s' %
          cur_time, color, cur_time_font)


# 给信息加上编号，输出列表
def inf_list(inf_orgin):
    inf_after = []
    for num, single_info in enumerate(inf_orgin):
        inf_after.append(u'%s、%s' % ((num + 1), single_info))
    return inf_after


def old_to_new_list(oldlist, linewith):
    newlist = []
    for single_text in oldlist:
        if font.getsize(single_text.strip())[0] < 750 or font.getsize(single_text.strip()) == 750:
            newlist.append(single_text)
        else:

            strList = []
            newStr = ''
            index = 0
            for item in single_text:
                newStr += item
                if font.getsize(newStr.strip())[0] > 750:
                    newlist.append(newStr[:-1])
                    newStr = ''
                    if font.getsize(single_text[index:])[0] < 750:
                        newlist.append(single_text[index:])
                    else:
                        break

                index += 1
    print(newlist)
    return newlist


# 绘制列表


def draw_info(x, y, the_list, linehigh, title_text):
    draw.text((x, y), u'%s' % (title_text), color, font)
    for num, info in enumerate(the_list):
        height = num * linehigh
        draw.text((x, y + height + 80), u'%s' % (info), color, font)


linewith = 21
linehigh = 80
p_fenge = 120

# 绘制科技
keji_x = title_x - 30
keji_y = title_y + 88
title_text = '【科技新闻】'
keji_text = a[1:gn:2]
keji_newlist = old_to_new_list(keji_text, linewith)
draw_info(keji_x, keji_y, keji_newlist, linehigh, title_text)

# 绘制国内
county_x = title_x - 30
county_y = title_y + 88 + linehigh * len(keji_newlist) + p_fenge
title_text = '【国内新闻】'
county_text = get_text(a[gn + 1])
county_oldlist = inf_list(county_text)
county_newlist = old_to_new_list(county_oldlist, linewith)
draw_info(county_x, county_y, county_newlist, linehigh, title_text)

# 绘制海外
ocean_x = title_x - 30
ocean_y = county_y + linehigh * len(county_newlist) + p_fenge
title_text = '【海外新闻】'
ocean_text = get_text(a[hw + 1])
ocean_oldlist = inf_list(ocean_text)
ocean_newlist = old_to_new_list(ocean_oldlist, linewith)
draw_info(ocean_x, ocean_y, ocean_newlist[0:10], linehigh, title_text)

# 绘制融资
CBD_x = title_x - 30
CBD_y = ocean_y + linehigh * len(ocean_newlist[0:10]) + p_fenge
title_text = '【融资收购】'
CBD_text = get_text(a[rz + 1])
CBD_oldlist = inf_list(CBD_text)
CBD_newlist = old_to_new_list(CBD_oldlist, linewith)
draw_info(CBD_x, CBD_y, CBD_newlist[0:10], linehigh, title_text)


# 生成图片
image.save(new_img, 'jpeg')

# 压缩图片
sImg = Image.open(new_img)
w, h = sImg.size
width = int(w / 2)
height = int(h / 2)
dImg = sImg.resize((width, height), Image.ANTIALIAS)
dImg.save(compress_img, 'jpeg')

#发送入保给好友
from wxpy import *
import time
#获取系统时间
cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#初始化
bot = Bot()
myfriends = bot.friends().search(u'小詹同学')[0]
myfriends.send(u'python自动早报到了 ' + cur_time)
myfriends.send_image('daily2.jpeg')

# groups = ['test',
#           '[禁推]小詹学Python交流①群',
#           '[禁推]小詹学Python交流②群',
#           '[禁推]小詹学Python交流③群',
#           '[禁推]小詹学Python交流④群',
#           '[禁推]小詹学Python交流⑤群',
#           '[禁推]小詹学Python交流⑥群',
#           '[禁推]小詹学Python交流⑦群',
#           '[禁推]小詹学Python交流⑧群']
# for send_OBJ in groups:
#     my_groups = bot.groups().search(groups)[0]
#     my_groups.send('python自动早报到了 ' + cur_time)
#     my_groups.send_image('daily2.jpeg')

