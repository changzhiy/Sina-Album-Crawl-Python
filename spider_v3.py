import re
from lxml import etree
import requests
import setting
import os

# 下次直接不用etree找模块了，因为有时候网站会出现一点不同，如果把界限卡得太死容易漏掉很多信息，所以直接把网页返还

user_agent = {
    'User-Agent' : setting.user_agent,
    'cookie' : setting.cookie,
}


def request_page(): # 保存某个相册的全部图片
    #  下面代码有bug， type = 3 则一直返回默认相册，无论album_id是多少,目前不知道怎么解决，所以只保存默认相册
    print("正在保存相册图片")
    page = 1 # 先前往第一页
    url = "https://photo.weibo.com/photos/get_all?uid=" + setting.uid + "&count=30&page="+str(page) + "&type=3"

    response = etree.HTML(requests.get(url,headers=user_agent).content)
    p_tag = str(etree.tostring(response)) # 获得p标签下的文本

    if len(p_tag) > 0:
        total_photo = int(re.findall('total..(.*?)..p', p_tag, re.S)[0])  # 相册下照片总数
        print("本相册共:" + str(total_photo) + "张图片")

        while total_photo/30 and total_photo > 0:
            # 由于page每次需要改变，所以不能调用上方的url，不然会循环一页下载
            url = "https://photo.weibo.com/photos/get_all?uid=" + setting.uid + "&count=30&page=" + str(page) + "&type=3"
            print("相册的第:" + str(page) + "页正在被下载")

            response = etree.HTML(requests.get(url, headers=user_agent).content)
            content_tag = str(etree.tostring(response))  # 获得a标签下的文本

            name_list = re.findall('pic_name...(.*?)...pic_', content_tag, re.S)
            for p in name_list:  # p 为pic_name
                save_img(p)

            total_photo -= 30
            page += 1

        if total_photo % 30 != 0:
            response = etree.HTML(requests.get(url, headers=user_agent).content)
            a_tag = str(etree.tostring(response))  # 获得a标签下的文本

            name_list = re.findall('pic_name...(.*?)...p', a_tag, re.S)
            for p in name_list:  # p 为pic_name
                    save_img(p)



def save_img(pic_name):  # 定义一个存图函数就可以了
    result = requests.get("https://wx4.sinaimg.cn/large/" + pic_name)
    file_path = "images/" + setting.uid + "/" + pic_name
    with open(file_path, 'wb') as f:
        # 写入本地
        f.write(result.content)
    print("图片:" + pic_name + "保存成功")


if __name__ == '__main__':
    if os.path.exists('images/{}'.format(setting.uid)):
        print('ID目录存在')
        pass
    else:
        print('ID目录不存在')
        os.mkdir('images/{}'.format(setting.uid))
        print('创建ID目录成功')

    request_page()