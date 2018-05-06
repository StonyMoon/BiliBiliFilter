import requests
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Text, Integer, String
from sqlalchemy import Column
import threading
import queue

DB_CONNECT_STRING = 'mysql+pymysql://root:root@localhost/danmu?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
BaseModel = declarative_base()


class Danmu(BaseModel):
    def __init__(self, user, content):
        self.user = user
        self.content = content

    __tablename__ = 'danmu'
    id = Column(Integer, primary_key=True)
    user = Column(String(16))
    content = Column(String(4096))


BaseModel.metadata.create_all(engine)


class Spider:
    def __init__(self, num):
        self.num = num
        self.threads = []
        self.crawl_queue = queue.Queue()

    def get_dammu(self, url):
        text = requests.get(url).text
        tree = ET.fromstring(text)
        danmu = [x for x in tree if x.tag == 'd']
        for each in danmu:
            user = each.get('p').split(',')[6]
            content = each.text
            session.add(Danmu(user, content))
        session.commit()

    def get_danmu_url(self, av):
        url = 'https://www.bilibili.com/video/av' + str(av)
        re = requests.get(url).text
        index = re.find('cid=') + 4
        i = 0
        while re[index + i].isdigit():
            i += 1
        cid = re[index:index + i]
        return 'https://comment.bilibili.com/' + cid + '.xml'

    def __call__(self, av=1, *args, **kwargs):
        for i in range(av, 2000000):
            self.crawl_queue.put(i)
        # 在这里开线程
        while self.threads or self.crawl_queue:
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)
            while len(self.threads) < 30 and self.crawl_queue:
                thread = threading.Thread(target=self.process_queue())
                self.threads.append(thread)
                thread.start()

    # 多线程执行的函数,处理队列
    def process_queue(self):
        av = self.crawl_queue.get()
        try:
            url = self.get_danmu_url(av)
            self.get_dammu(url)
            print('爬取%s成功' % av)
        except:
            print('爬取%s失败' % av)
            session.rollback()


spider = Spider(1)
spider(1792)
