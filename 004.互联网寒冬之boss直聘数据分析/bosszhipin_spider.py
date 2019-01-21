import csv
import re
import requests
from time import sleep
from random import uniform
from urllib.parse import urlencode
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BOSS_spider():
    def __init__(self):
        self.browser = webdriver.Chrome()

    def get_page(self,start_url=1,number=10):
        base_url = 'https://www.zhipin.com/c101010100/?query=%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89&'
        for i in range(start_url,start_url+number):
            data = {
                'page': i,
                'ka': 'page-{}'.format(i)
            }
            url = base_url + urlencode(data)
            print(url)
            self.browser.get(url)
            try:
                WebDriverWait(self.browser, timeout=10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'next'))
                )  # 等待next页面的信息全部加载完毕，在进行下一步的操作。
            except TimeoutError:
                print('工作列表页提取失败，重新获取')
                self.browser.get(url)
            text = self.browser.page_source  # 页面提取
            self.get_job_url(text)  # 解析页面工作url链接

    def get_job_url(self,text):
        url_list = []
        if text:
            soup = BS(text, 'lxml')
            divs = soup.find_all(class_='job-primary')
            for div in divs:
                s_url = 'https://www.zhipin.com/' + div.a['href']
                url_list.append(s_url)
            for url in url_list:
                self.parse_job(url)

    def parse_job(self,url):  # 解析每一个页面的提取信息
        self.browser.execute_script(r'window.open("{}")'.format(url))#打开url的界面
        self.browser.switch_to.window(self.browser.window_handles[1])#浏览器跳转到新打开的界面当中
        try:
            WebDriverWait(self.browser, timeout=10, ).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="name"]/h1'))
            )
            text = self.browser.page_source#返回页面源代码
            self.get_content(text)  # 获取需要的内容
            sleep(uniform(3, 8))  # 模拟用户浏览网页
            self.browser.close()  # 关将新的窗口关闭
            self.browser.switch_to.window(self.browser.window_handles[0])  # 切换第一个页面
        except:
            sleep(uniform(30, 60))  # 等待输入验证码时间
            print('详情页提取失败... 重新提取')
            self.browser.close()  # 关闭新窗口
            self.browser.switch_to.window(self.browser.window_handles[0])  # 切换第一个页面
            self.parse_job(url)

    def get_content(self,text):
        data = {}
        # res = requests.get(url1, headers=headers)
        patten = re.compile('<p>城市：(.*?)<em class="vline"></em>经验：(.*?)<em class="vline"></em>学历：(.*?)</p>')
        result = re.findall(patten, text)
        soup = BS(text, 'lxml')
        badge = soup.find('span', class_='badge')
        if badge:
            badge = badge.text
        else:
            badge = None
        # company = soup.find('h3', class_='name').text
        company = soup.find('h3',class_='name').text
        require1 = soup.find('div', class_='text')
        if require1:
            require = require1.text
        else:
            require = ''

        if result:
            if len(result[0]) == 3:
                data['地点'] = result[0][0]
                data['经验'] = result[0][1]
                data['学历'] = result[0][2]
                # print(badge)
                if badge:
                    data['工资'] = badge.strip()
                else:
                    data['工资'] = None

                data['公司'] = company
                data['工作要求'] = require.strip()

        self.save_data_csv(data)

    def save_title(self):
        title = ['地点', '经验', '学历', '工资', '公司', '工作要求']
        with open('boss_ZP1.csv', 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, title)
            writer.writeheader()

    def save_data_csv(self, data):
        # print(data['公司'])
        with open('boss_ZP1.csv', 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            title = ['地点', '经验', '学历', '工资', '公司', '工作要求']
            writer.writerow([data[i] for i in title])
        print('*' * 10 + '保存成功' + '*' * 10)

    def start(self):
        self.save_title()
        self.get_page()
        print()


if __name__ == '__main__':
    spider = BOSS_spider()
    # url = 'https://www.zhipin.com/job_detail/?query=python&scity=100010000&industry=&position='
    spider.start()

