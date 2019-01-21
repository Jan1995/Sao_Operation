import requests
from lxml import etree
import random
import time
from openpyxl import Workbook


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

FILENAME = 'demo_anjuke.xlsx'


def get_areas(url):
    response = etree.HTML(requests.get(url, headers=HEADERS).text)
    areas = response.xpath('//div[@class="sub-items sub-level1"]/a/text()')[1:]
    areas_link = response.xpath('//div[@class="sub-items sub-level1"]/a/@href')[1:]
    print(areas)
    wb = Workbook()

    for area, area_link in dict(zip(areas, areas_link)).items():
        print(area)
        ws = wb.create_sheet(area)
        ws.append(['位置1', '位置2', '位置3', '位置4', '户型', '面积（平米）', '楼层', '其他', '价格（元/月）'])
        page = 1
        get_infos(area_link, ws, page)
        print('')

    wb.save(FILENAME)


def get_infos(url, ws, page):
    print('page ---> {}   '.format(page), end='\r')
    response = etree.HTML(requests.get(url, headers=HEADERS).text)
    items = response.xpath('//div[@class="zu-itemmod  "]')
    for item in items:
        detail = item.xpath('.//p[@class="details-item tag"]/text()')
        room_type = detail[0].split()[0]
        area = detail[1][:-2]
        floor = detail[2]
        address_1, address_2, address_3, address_4 = None, None, None, None
        address = item.xpath('.//address[@class="details-item"]//text()')
        try:
            address_1 = address[1]
        except:
            pass
        address = address[-1].split()
        try:
            address_2 = address[0].split('-')[0]
            address_3 = address[0].split('-')[1]
        except:
            pass
        try:
            address_4 = address[1]
        except:
            pass
        detail_2 = item.xpath('.//p[@class="details-item bot-tag clearfix"]//text()')
        other = ' '.join(detail_2[1::2])
        price = item.xpath('.//div[@class="zu-side"]/p/strong/text()')[0]

        ws.append([address_1, address_2, address_3, address_4, room_type, area, floor, other, price])

    time.sleep(random.random())
    next_page = response.xpath('//a[@class="aNxt"]')
    if next_page:
        page += 1
        get_infos(next_page[0].xpath('./@href')[0], ws, page)


if __name__ == '__main__':
    url = 'https://hz.zu.anjuke.com/'
    get_areas(url)
