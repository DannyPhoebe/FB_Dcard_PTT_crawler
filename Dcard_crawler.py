from Dcard_config import header,default_len,forum,until
from util import lencheck,page_load
import requests
import re
import json
import time
import datetime


class Dcard_crawler(object):
    
    def __init__(self, header=header,default_len=default_len,forum=forum,until=until, sleep=True):
        self.forumlist = ['timecapsule','relationship','girl','makeup','dressup','funny','rainbow','marvel','boy','horoscopes','food','mood','travel']
        self.forum = forum
        self.init_url = "https://www.dcard.tw/f/{}".format(forum) if forum in self.forumlist else None
        self.until = until if until <= str(datetime.datetime.now())[0:10] else str(datetime.datetime.now())[0:10]
        self.default_len = default_len
        self.sleep = sleep
        self.post_ids = list()
        self.url_num = None
        self.data = dict()
        print("Dcard_crawler is activated...")
    
    def pid_collector(self):
        assert self.init_url,"the forum you type doesn't exist"
        page = json.loads(re.search('\"store\"\:(\[.+\"anonymousDepartment\"\:.+?\}\])',requests.get(self.init_url,headers=header).text).group(1))
        self.post_ids.append([item['id'] for item in page])
        if lencheck(page) == self.default_len: # first page hasn't reach the end
            while True:
                iter_id = page[-1]['id']
                url = 'https://www.dcard.tw/_api/forums/{}/posts?popular=false&before={}'.format(self.forum,iter_id)
                page = page_load(url) if lencheck(page)==self.default_len else page_load(url,end=lencheck(page))
                self.post_ids.append([item['id'] for item in page])
                if self.sleep:
                    time.sleep(2)
                if len(page) != self.default_len:
                    break
        self.post_ids = sum(self.post_ids,[])
        self.url_num = len(self.post_ids)
        print(len(self.post_ids),"post urls are collected")
        
        
    def crawler(self):
        assert len(self.post_ids) > 0,'please run pid_collector first'
        self.data['info'] = {'until':self.until}
        self.data['post'] = [None]*self.url_num
        for idx,pid in enumerate(self.post_ids):
            # start of post crawler
            print('crawling post {}...'.format(idx))
            p_url = 'https://www.dcard.tw/f/travel/p/{}'.format(pid)
            p_res = requests.get(p_url,headers=header)
            pos = json.loads(re.search('\"store\"\:\[(.+?\"anonymousDepartment\"\:.+?\})\]',p_res.text).group(1))
#                 if idx%1 == 0:
            time.sleep(2)
            # start of comment crawler
            total_pages = pos['commentCount']//30 + 1
            c_urls = ['https://www.dcard.tw/_api/posts/{}/comments?after={}'.format(pid,page*30) for page in range(total_pages)]
            c_res = [page_load(c_url) for c_url in c_urls]
            pos['comments'] = sum(c_res,[])
            self.data['post'][idx] = pos
        with open('result.json', 'w', encoding='utf-8') as fp:
            json.dump(self.data, fp)
        print('process complete.')