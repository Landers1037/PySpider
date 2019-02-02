'''抓取猫眼电影的排行前100'''
import json

import requests
import re
#抓取链接 https://maoyan.com/board/4
#分析html可以写出对应的正则表达式

def get_one_page(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        return response.text
    return None



def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>'
                       '.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield { #类似一个迭代器，每次返回一个值（字典）
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:] if len(item[3])>3 else '',
            'time' :item[4].strip()[5:] if len(item[4])>5 else '',
            'score':item[5].strip()+item[6].strip()

        }
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8')as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content,ensure_ascii=False)+'\n')


def main(offset):
    url='https://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    # print(html)
    parse_one_page(html)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__=='__main__':
    for i in range(10):
        main(offset=i*10)
