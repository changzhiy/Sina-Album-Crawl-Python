# 首先要通过旧网址打开需要爬取的用户相册
# 查询需要爬取用户的相册id
# 网址：'https://photo.weibo.com/' + uid + '/talbum/index',

# @author githubId:Cool-CoCoder
import requests
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import uuid
import math
import sys

# 当微博更新时，要更改cookie和refer（通过XHR获取），params参数要改

print("以下数据请通过xhr查询")
uid = input("输入微博ID:")  # 输入微博ID
cookie = input("输入cookie:")  # 输入cookie
album_id = input("输入相册id:")  # 输入相册id
_rnd = input("输入_rnd:")  # 输入_rnd
photos_num = int(input("请输入该相册照片数:"))  # 输入照片数
location = input("输入存储位置:")  # 存储位置 形如 'D:/微博/欧阳娜娜相册'

# 相册页数，一页30张
pages_num = math.ceil(photos_num/30)
print("共有" + str(pages_num) + "页照片，您需要存储哪些部分呢？")
start_page = int(input("输入起始页码:"))
end_page = int(input("请输入结束页码:"))

# 拼接成headers
headers = {
    'Referer': 'https://photo.weibo.com/' + uid + '/talbum/index',
    'cookie': cookie,
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36'
}

'''
参数: params 访问链接的参数
返回值: 照片id的列表
'''


def get_photos_link_list(params):
    # 初始访问链接
    firs_request_url = 'https://photo.weibo.com/photos/get_all?' + urlencode(params)

    # 通过Fn+F12中的网络 XHR 中的 answer？的请求URL
    r = requests.get(firs_request_url, headers=headers)

    # 选择lxml作为解析器
    soup = BeautifulSoup(r.content, 'lxml')
    string_contain_photos = str(soup)

    # 正则表达式获得照片id
    raw_image_link = re.findall('photo_id\"\:\"(.*?)\"\,\"pic', string_contain_photos, re.S)
    return raw_image_link


'''
获得图片的初始链接，调用get_photos_link_list(params)
参数：page 第几页
'''


def get_raw_image_link(page):
    params = {
        'uid': uid,
        'album_id': album_id,
        'count': '30',
        'page': page,
        'type': '3',
        '__rnd': _rnd
    }
    return get_photos_link_list(params)


'''
保存图片
参数： raw_image_link 为图片的id列表
'''


def save_picture(raw_image_link):
    for j in range(len(raw_image_link)):
        # 微博大图初始链接
        raw_photo_url = 'https://photo.weibo.com/' + uid + '/wbphotos/large/photo_id/{0}/{1}/{2}'.format(
            raw_image_link[j], 'album_id', album_id)
        r = requests.get(raw_photo_url, headers=headers)
        second_request_url = r.text
        image_url = re.findall('pic\" src=\"(.*?)\" onload', second_request_url, re.S)
        # image_url 形如 ['https://wx4.sinaimg.cn/large/002VTQLVly1go7nx7fvmqj60u01904qp02.jpg']
        # 由于特定的被删除照片会导致空指针,这里进行排错
        if len(image_url) < 1:
            print("该照片被删除")
        else:
            result = requests.get(image_url[0], headers=headers)
            # 生成唯一的uuid
            single_id = str(uuid.uuid1())
            # 文件地址
            file_path = '{0}/{1}.{2}'.format(location, single_id, 'jpg')
            with open(file_path, 'wb') as f:  # 写入
                f.write(result.content)
            # print("成功保存:" + image_url[0] + "到:" + file_path)


if __name__ == '__main__':
    for i in range(end_page - start_page + 1):
        # 进度条功能
        print("\r", end="")
        # 进度条比例
        print("Crawling progress: {:.2%}: ".format(i / (end_page - start_page)), "▋" * (i + 1), end="")
        save_picture(get_raw_image_link(start_page + i))
        sys.stdout.flush()
