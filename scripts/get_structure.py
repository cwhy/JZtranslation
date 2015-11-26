import re
import os
import os.path as op
import json
import requests
import glob

from html2text import html2text
from bs4 import BeautifulSoup

CACHE_DIR = op.join(op.pardir, 'cache')
CN_DIR = op.join(op.pardir, 'Chinese')
LIST_DIR = op.join(op.pardir, 'list.txt')
DICT_DIR = op.join(op.pardir, 'dictionary')


def jargon_translate(txt):
    dic = {}
    for file_ in glob.glob(op.join(DICT_DIR, '*.json')):
        with open(file_, 'r') as _f:
            _dict_file = _f.read()
        _dic = json.loads(_dict_file)
        dic.update(_dic)
    if dic:
        pattern = re.compile('|'.join(dic.keys()))
        result = pattern.sub(lambda x: dic[x.group()], txt)
        return result
    else:
        return txt


class Page(object):
    def __init__(self, url, cate):
        self.ID = url.split('?id=')[1]
        self.url = url
        self.category_id = cate.ID
        self.category_name = cate.name_CN
        path_raw = op.join(cate.path, 'raw', self.ID)

        if os.path.isfile(path_raw):
            with open(path_raw, 'r') as _f:
                _content = _f.read()
        else:
            with open(path_raw, 'w') as _f:
                response = requests.get(url)
                response.encoding = 'GBK'
                _content = response.text
                _f.write(_content)
        soup = BeautifulSoup(_content, 'lxml')
        self.title = soup('div', class_='sub_right_ltlt')[0].span.contents[0]
        self.author = soup('div', class_='sub_right_ltlb')[0].a.contents[0]
        content_html = str(soup('div', class_='sub_right_lb')[0])
        base_url = 'http://www.swarma.org/swarma/'
        self.content = html2text(content_html, baseurl=base_url)
        self.content = jargon_translate(self.content)
        self.path = op.join(CN_DIR, self.ID)

    def save(self):
        with open(self.path + '.md', 'w') as _f:
            _f.write(self.content)
        self.content = self.path + '.md'

        with open(self.path + '.json', 'w') as _f:
            _f.write(self.toJson())

    def toJson(self):
        return json.dumps(
            self.__dict__,
            ensure_ascii=False,
            indent=2)

    def __str__(self):
        return self.toJson()

    def __repr__(self):
        return self.__str__()


class Cate(object):
    def __init__(self, raw):
        lines = raw.split('\n')
        self.ID = re.search(r'[\d\s]+', lines[0]).group().strip()
        self.name_CN = lines[0].split(self.ID)[1].strip()
        self.links = [l for l in lines[1:] if l]

        self.path = op.join(CACHE_DIR, 'Cate', self.ID)
        self.create_file_str()
        pages = [Page(l, self) for l in self.links]
        for page in pages:
            page.save()

    def create_file_str(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        os.makedirs(op.join(CACHE_DIR, 'Cate'), exist_ok=True)
        os.makedirs(self.path, exist_ok=True)
        os.makedirs(op.join(self.path, 'raw'), exist_ok=True)

    def toJson(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def __str__(self):
        return self.toJson()

    def __repr__(self):
        return self.__str__()


with open(LIST_DIR, 'r') as f:
    content = f.read()
cats_raw = content.split('\n\n')
cats = [Cate(cr) for cr in cats_raw]
