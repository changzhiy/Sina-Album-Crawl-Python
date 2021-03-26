# 首先查询需要爬取用户的相册id
# 要通过旧网址打开需要爬取的用户相册
# 网址：'https://photo.weibo.com/' + uid + '/talbum/index',
# @author github-Id:Cool-CoCoder

# 引入协程，python多线程为假的多线程，但协程可以同步执行，总的来说换汤不换药，而且使用比较简单
from gevent import monkey
import gevent
# 协程爬虫需要monkey补丁，并且要在import 之前
monkey.patch_all()
# 导入协程池
from gevent.pool import Pool
import requests
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import uuid
import math
import sys
# 使用多个agent访问，避免触发服务器反爬机制
from fake_useragent import UserAgent

# --------------------------------------------------------------------------------------------------
# 程序所需信息
print("以下数据请通过xhr查询")
uid = input("输入微博ID:")  # 输入微博ID
cookie = input("输入cookie:")  # 输入cookie
album_id = input("输入相册id:")  # 输入相册id
_rnd = input("输入_rnd:")  # 输入_rnd
photos_num = int(input("请输入该相册照片数:"))  # 输入照片数
location = input("输入存储位置:")  # 存储位置 形如 'D:/微博/欧阳娜娜相册'

# 相册页数，一页30张
pages_num = math.ceil(photos_num / 30)
print("共有" + str(pages_num) + "页照片，您需要存储哪些部分呢？")
start_page = int(input("输入起始页码:"))
end_page = int(input("请输入结束页码:"))

# --------------------------------------------------------------------------------------------------

# 执行逻辑 save_picture 调用 get_raw_image_link 调用 get_raw_image_link 调用 get_photos_link_list 调用 get_header

# --------------------------------------------------------------------------------------------------


# 实例化userAgent
ua = UserAgent()
# 拼接成headers
'''
获取headers，且headers随机变换，模拟多主机访问
'''


def get_header():
    headers = {
        'Referer': 'https://photo.weibo.com/' + uid + '/talbum/index',
        'cookie': cookie,
        'user-agent': ua.random
    }
    return headers


'''
参数: params 访问链接的参数
返回值: 照片id的列表
'''


def get_photos_link_list(params):
    # 初始访问链接
    firs_request_url = 'https://photo.weibo.com/photos/get_all?' + urlencode(params)

    r = requests.get(firs_request_url, headers=get_header())

    # 选择lxml作为解析器
    soup = BeautifulSoup(r.content, 'lxml')
    string_contain_photos = str(soup)
    # 防止被认为恶意攻击，要对访问进行关闭
    r.close()

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
        # 单个线程进度条比例
        print(str(gevent.getcurrent()) + "的进度: {:.2%}: ".format(j / (len(raw_image_link) - 1)), "▋" * (j + 1))
        sys.stdout.flush()
        # 微博大图初始链接
        raw_photo_url = 'https://photo.weibo.com/' + uid + '/wbphotos/large/photo_id/{0}/{1}/{2}'.format(
            raw_image_link[j], 'album_id', album_id)
        # 包裹try except
        try:
            r = requests.get(raw_photo_url, headers=get_header())
            second_request_url = r.text
            image_url = re.findall('pic\" src=\"(.*?)\" onload', second_request_url, re.S)

            # 防止远程主机关闭连接，要进行close
            r.close()

            # image_url 形如 ['https://wx4.sinaimg.cn/large/002VTQLVly1go7nx7fvmqj60u01904qp02.jpg']
            # 由于特定的被删除照片会导致空指针,这里进行排错
            if len(image_url) < 1:
                print("该照片被删除")
            else:
                result = requests.get(image_url[0], headers=get_header())
                # 生成唯一的uuid
                single_id = str(uuid.uuid1())
                # 文件地址
                file_path = '{0}/{1}.{2}'.format(location, single_id, 'jpg')
                with open(file_path, 'wb') as f:
                    # 写入本地
                    f.write(result.content)
        except Exception as e:
            print("出现异常为:" + e)


if __name__ == '__main__':
    # 创建协程池，数量适中就可以
    # 线程多了可以提高程序并行执行的速度，但是并不是越多越好，其中，每个线程都要占用内存，多线程就意味着更多的内存资源被占用，其二，从微观上讲，一个cpu不是同时执行两个线程的，他是轮流执行的，所以线程太多，cpu必须不断的在各个线程间快回更换执行，线程间的切换无意间消耗了许多时间，所以cpu有效利用率反而是下降的
    thread_pool = Pool(50)
    for i in range(end_page - start_page + 1):
        # 进度条比例
        print("线程启动进度: {:.2%}: ".format(i / (end_page - start_page)), "▋" * (i + 1))

        # 通过协程池创建线程，执行方法，协程池采用排队策略，非常便于使用
        thread_pool.spawn(save_picture, (get_raw_image_link(start_page + i)))
        sys.stdout.flush()

    # for循环之后，协程池还有部分未执行结束的协程，等待协程全部执行结束然后告知用户
    thread_pool.join()
    print("代码执行结束~")

