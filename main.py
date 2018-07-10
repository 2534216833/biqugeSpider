import requests
import sys
from bs4 import BeautifulSoup
import re


class downloader(object):
    def __init__(self, name):
        self.name = name
        self.server = 'https://www.qu.la'
        self.target = 'https://www.qu.la/book/'
        self.bookID = 0
        self.names = []  # 章节名
        self.urls = []  # 存放章节链接
        self.nums = 0  # 章节数
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    def getBook(self):
        req = requests.get(
            'https://sou.xanbhx.com/search?siteid=qula&q='+self.name, headers=self.headers)
        try:
            rebs = BeautifulSoup(req.text, 'lxml').find_all(
                'li')[1].find('span', class_='s2').find('a').get('href')
            self.bookID = re.findall(r'book/(.*)/', rebs)[0]
            self.target = self.target+str(self.bookID)
            print("已找到该书")
        except BaseException:
            print("无该书，重新输入书名")

    def getDownload(self):
        self.getBook()
        req = requests.get(url=self.target, headers=self.headers)
        urlbs = BeautifulSoup(req.text, 'lxml')
        a = urlbs.find('div', id='list').find_all('a')[12:]
        self.nums = len(a)
        for each in a:
            self.names.append(each.string)
            self.urls.append(self.server+each.get('href'))

    def getContents(self, target):
        re = requests.get(url=target, headers=self.headers)
        content = BeautifulSoup(re.text, 'lxml').find(
            'div', id='content').text.replace('\t', '').replace('\u3000'*4, '\n\n')
        return content

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == "__main__":
    name = input("输入要下载的小说名:")
    dl = downloader(name)
    dl.getDownload()
    print('开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i], name+'.txt', dl.getContents(dl.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" % float(i/dl.nums) + '当前章节：'+dl.names[i]+ '\r')
        sys.stdout.flush()
    print('下载完成')

