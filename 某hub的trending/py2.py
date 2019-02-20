# pohub的图片爬虫
from pyquery import PyQuery as pq
import json
import os
import requests

# data = []

def save(ul,a):
    if not os.path.exists('hotvideo'):
        os.mkdir('hotvideo')
    if ul:
        filepath = '{0}/{1}.{2}'.format('hotvideo','pic'+str(a),'jpg')
        content = requests.get(ul).content
        if not os.path.exists(filepath):
            with open(filepath,'wb')as file:
                file.write(content)


def get_page(url):
    a=0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.80 Safari/537.36'}
    html = requests.get(url,headers).text
    doc = pq(html)
    # print(html)
    # images = doc('#hotVideosSection').items()  # 当前的id后面所有的元素获取
    images = doc('.phimage').items()
    for image in images:

        # list = {}
        # img = image.find('img').attr('src')

        # img = image.find('.img img').attr('data-mediumthumb') # 抓取中等大小的缩略图
        img = image.find('img').attr('data-src') # 为了避免gif文件的冲突

        print(img)
        # save(img,a)
        a += 1
        # list['img'] = img
        # data.append(list)

    # print(data)


if __name__=='__main__':
    url = 'https://www.pornhub.com'
    # get_page(url)
    video = requests.get('https://cv.phncdn.com/videos/201901/25/203634301/720P_1500K_203634301.mp4?JxndJYPDVkLztlzpMjhqGegRHu9T2WB2vHls8Zy3V0UUhkaj1eHrRY4Cbn8m_v9zZxRoAO2oxHXXNCkvRqHbcGzleQ_ikyHukP2XNswlHXAC2p-ZB_iaimBgd_aoCzSLZ0VTFsyIdo77CfaPiDbIxz5J6PwVn3lEwB5W7HbOKaWWvrXS4IuweHmMhdO1OA1nDOcVYjlrYM0').content
    with open('1.mp4','wb')as f:
        f.write(video)