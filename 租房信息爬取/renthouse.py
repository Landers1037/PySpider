# 租房中介信息爬取
# 可以选择房源信息 ，默认安居客，可选58同城

import csv
import requests
from pyquery import PyQuery as pq
import pymysql
import json
print('安居客房源按1，58同城按2\n')


list=[]

def get_anjukepage(offset):
    url='https://xy.zu.anjuke.com/fangyuan/xiangchengbc/p'+str(offset)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.80 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    doc = pq(html)
    items = doc('.zu-itemmod').items()
    for item in items:
        data = {}
        data['位置'] = item.find('.zu-info a').text()
        data['大小'] = item.find('.zu-info p').text().replace('\n','')
        data['价格'] = item.find('.zu-side').text().replace('元/月','')
        data['单位'] = '元/月'
        list.append(data)

def get_58page(offset):
    url = 'https://xf.58.com/xiangcheng/zufang/pn'+str(offset)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.80 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    doc = pq(html)
    items = doc('.des').items()
    moneys = doc('.money').items()
    for item,money in zip(items,moneys):
        data = {}
        data['位置'] = item.find('a').text()
        data['大小'] = item.find('p').text()
        data['价格'] = money.find('b').text().replace('元/月','')
        # data['单位'] = '元/月'
        list.append(data)

def save():
    headers = ['位置', '大小', '价格','单位']
    with open('C:\\Users\Administrator\Desktop\租房信息.csv', 'w',encoding='gb18030')as file:

        file_csv = csv.DictWriter(file, headers)
        file_csv.writeheader()
        file_csv.writerows(list)

def csv2sql():
    # data = pd.read_csv('house.csv',encoding='gbk')
    # data = {
    #     '位置': '舔狗',
    #     '大小': '200',
    #     '价格': '2000'
    # }
    # 位置 = '天使'
    # 大小 = '200'
    # 价格 = '515'

    with open('list.json','r',encoding='utf-8')as f:
        load_dict = json.load(f)
    # print(load_dict)

    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')
    cursor = db.cursor()  # 操作的游标
    # sql = 'CREATE TABLE IF NOT EXISTS house (位置 VARCHAR(255) NOT NULL,大小 VARCHAR (30) NOT NULL,价格 VARCHAR(30) NOT NULL'
    # cursor.execute(sql)
    # length = len(data)
    # for i in range(0,length):
    #     record = tuple(data)
    #     try:
    #         sqlSentence4 = "insert into house (位置, 大小, 价格) ,values (%s,%s,%s)"
    #         # 获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
    #         cursor.execute(sqlSentence4,data)
    #     except:  # 如果以上插入过程出错，跳过这条数据记录，继续往下进行
    #         break

    sql = 'insert ignore into house(位置, 大小 ,价格) values(%s,%s,%s)'
    for i in range(0,len(load_dict)):
        data = load_dict[i]
        print(data)
        cursor.execute(sql,(data['位置'] ,data['大小'] ,data['价格']))
    db.commit()
    cursor.close()


def main(num):
    if num == 2:
        for i in range(40):
            try:
                get_58page(i)

            except Exception as e:
                print('部分数据获取失败')

    elif num == 1:
        for i in range(40):
            try:
                get_anjukepage(i)
            except Exception as e:
                print('部分数据获取失败')


if __name__ == '__main__':
    # num = int(input('输入：\n'))
    # main(num)
    # save()
    csv2sql()
