import requests
from pyquery import pyquery
import xml.etree.ElementTree as ET


class Danmu:
    def __init__(self, user, content):
        self.content = content
        self.user = user


def get_danmu_url(url):
    re = requests.get(url).text
    index = re.find('cid=') + 4
    i = 0
    while re[index + i].isdigit():
        i += 1
    cid = re[index:index + i]
    return 'https://comment.bilibili.com/' + cid + '.xml'


# 返回弹幕列表
def get_dammu(url):
    text = requests.get(url).text
    tree = ET.fromstring(text)
    danmu = [x for x in tree if x.tag == 'd']
    result = []
    for each in danmu:
        user = each.get('p').split(',')[6]
        content = each.text
        result.append(Danmu(user, content))
    return result


def get_foolish_user_list(danmu_list, foolish_danmu):
    foolish_users = []
    fil = filter(lambda danmu: foolish_danmu in danmu.content, danmu_list)
    for each in fil:
        foolish_users.append(each.user)
    foolish_users = list(set(foolish_users))
    return foolish_users


def output_xml(users):
    s = '<filters>\n'
    for user in users:
        s += '<item enabled="true">u=' + user + '</item>\n'
    s += '</filters>'
    return s
    # with open('filter.xml', 'w') as f:
    #     f.write('<filters>\n')
    #     for user in users:
    #         f.write('<item enabled="true">u=')
    #         f.write(user)
    #         f.write('</item>\n')
    #     f.write('</filters>')


def get_user_by_danmu(url, keyword):
    url1 = get_danmu_url(url)
    danmu = get_dammu(url1)
    users = get_foolish_user_list(danmu, keyword)
    return output_xml(users)

#
# print('根据视频中弹幕内容来产生屏蔽名单')
# print('比如屏蔽\'坐飞机\'')
# print('如果有用户在这个视频中发的弹幕含有\'坐飞机\'，则这个用户就会被导入屏蔽列表中')
# av = input('请输入av号(例如 av12345)：')
# key = input('请输入需要屏蔽的关键词：')
# url = 'https://www.bilibili.com/video/' + av
# get_user_by_danmu(url, key)
#
# input('导出成功，按任意键退出')
