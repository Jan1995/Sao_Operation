#_*_ coding:utf8 _*_
import requests
import json
import csv
import time
global auctions_distinct
auctions_distinct = []

def get_auctions_info(response_auctions_info, file_name):
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in response_auctions_info:
            if str(i['raw_title']) not in auctions_distinct:
                writer.writerow([i['raw_title'], i['view_price'],i['view_sales'], i['nick'], i['item_loc']])
                auctions_distinct.append(str(i['raw_title']))
        csvfile.close()

if __name__ == '__main__':
    for k in ['内衣女', '内衣']:
      
        headers = {
            "Referer":"https://s.taobao.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "content-type": "application/json;charset=UTF-8",
            "accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
      
        }
        file_name = k + '.csv'
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['标题', '价格', '销量', '店铺', '区域'])
            csvfile.close()
        
        print('记得关注小詹公号：[小詹学python]噢')
        
        for p in range(88):
            #url = 'https://s.taobao.com/api?callback=jsonp227&m=customized&q=%s&s=%s' % (k, p)
            try:
                url = "https://s.taobao.com/api?_ksTS=1540273014777_279&callback=jsonp280&ajax=true&m=customized&stats_click=search_radio_all:1&q=%s&s=%s&imgfile=&initiative_id=staobaoz_20181023&bcoffset=-1&js=1&style=grid&ie=utf8&rn=2d60b78e90963e4e9fc4d50dff6e8cdb" % (k,p)
                r = requests.get(url,timeout=30,headers=headers)
                r.raise_for_status()
                r.encoding=r.apparent_encoding
                time.sleep(3)
                response = r.text
                #response = response.strip("/n")
                #response = response.split('(')
                #re.findall('g_page_config = (\{.+\})', data)[0]
                response = response.strip()
                response = response.split('(')[1].split(")")[0]
                #print(response.split('(')[1].split(")")[0])
                response_dict = json.loads(response)
                #print(response_dict)
                response_auctions_info = response_dict['API.CustomizedApi']['itemlist']['auctions']
                print(response_auctions_info)       
                get_auctions_info(response_auctions_info, file_name)
            except:
                print("耐心等待请求到某宝数据，可能得过一会才能得到数据噢")
    print('长度' , len(auctions_distinct))
