import requests
import time
from lxml import etree
import random
import re
from openpyxl import Workbook


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

FILENAME = 'demo_lianjia.xlsx'


def progress_bar(num, total):
    rate = int(100*num/total)
    print('[{}{}]{}%        '.format('*'*int(rate/2), ' '*int((100-rate)/2), rate), end='\r')


def get_areas(url):
    response = etree.HTML(requests.get(url, headers=HEADERS).text)
    areas = response.xpath('//dd[@data-index="0"]/div[@class="option-list"]//a/text()')[1:]
    areas_link = response.xpath('//dd[@data-index="0"]/div[@class="option-list"]//a/@href')[1:]

    wb = Workbook()

    for area, area_link in dict(zip(areas, areas_link)).items():
        url = 'https://hz.lianjia.com' + area_link
        get_pages(area, url, wb)

    wb.save(FILENAME)


def get_pages(area, url, wb):
    ws = wb.create_sheet(area)
    ws.append(['位置1', '位置2', '户型', '面积（平米）', '朝向', '楼层', '建造时间', '价格（元/月）'])

    response = requests.get(url, headers=HEADERS).text
    pages = int(re.findall("page-data=\'{\"totalPage\":(\d+),\"curPage\"", response)[0])

    print(area)
    for page in range(1, pages+1):
        try:
            get_infos(url + 'pg' + str(page), ws)
        except:
            pass
        progress_bar(page, pages)
        time.sleep(random.random())
    print('')  # 换行




def get_infos(url, ws):
    response = etree.HTML(requests.get(url, headers=HEADERS, timeout=5).text)
    items = response.xpath('//div[@class="info-panel"]')
    for item in items:
        place = item.xpath('./div[1]/div/a/span/text()')[0][:-2]
        room_type = item.xpath('./div[1]/div/span[@class="zone"]/span/text()')[0][:-2]
        area = item.xpath('./div[1]/div/span[@class="meters"]/text()')[0][:-4]
        postion = item.xpath('./div[1]/div/span[3]/text()')[0]
        place_2 = item.xpath('./div[1]/div[2]/div[@class="con"]/a/text()')[0][:-2]
        floor = item.xpath('./div[1]/div[2]/div[@class="con"]/text()')[0]
        time = item.xpath('./div[1]/div[2]/div[@class="con"]/text()')[1][:4]
        price = item.xpath('./div[2]/div/span/text()')[0]

        ws.append([place, place_2, room_type, area, postion, floor, time, price])


if __name__ == '__main__':
    url = 'https://hz.lianjia.com/zufang'  # 杭州租房
    get_areas(url)
