import requests
from pyquery import pyquery
import xml.etree.ElementTree as ET

class Danmu:
    def __init__(self,user,content):
        self.content = content
        self.user = user


def get_danmu_url(url):
    text = requests.get(url).text
    soup = pyquery.PyQuery(text)('#bofqi')
    for each in soup.items():
        cid = each.text().split('cid=')[1].split('&')[0]
        return 'https://comment.bilibili.com/'+cid+'.xml'


#返回弹幕列表
def get_dammu(url):
    text = requests.get(url).text
    tree = ET.fromstring(text)
    danmu = [x for x in tree if x.tag == 'd']
    result = []
    for each in danmu:
        user = each.get('p').split(',')[6]
        content = each.text
        result.append(Danmu(user,content))
    return result


def get_foolish_user_list(danmu_list,foolish_danmu):
    foolish_users = []
    fil = filter(lambda danmu:foolish_danmu in danmu.content, danmu_list)
    for each in fil:
        foolish_users.append(each.user)
    foolish_users = list(set(foolish_users))
    return foolish_users


def output_xml(users):
    with open('filter.xml','w') as f:
        f.write('<filters>\n')
        for user in users:
            f.write('<item enabled="true"> u=')
            f.write(user)
            f.write('</item>\n')
        f.write('</filters>')



def get_user_by_danmu(url,keyword):
    url = get_danmu_url(url)
    danmu = get_dammu(url)
    users = get_foolish_user_list(danmu,keyword)
    output_xml(users)



get_user_by_danmu('https://www.bilibili.com/video/av19856920/','茶')



