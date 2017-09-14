import re
import requests
from bs4 import BeautifulSoup

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class ChineseDetected(object):
    _re = None

    def __init__(self):
        self._re = re.compile('[\u4e00-\u9fa5]+')

    def get_count(self, s):
        chinese_list = self._re.findall(s)
        count = 0
        for c_item in chinese_list:
            count += len(c_item)
        return count

def getHTMLText(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return " "

def parsePage(ilt,ilt2,html):
    try:
        soup = BeautifulSoup(html,"html.parser")
        name = soup.find_all("p",{"class":"item-title"})
        name2 = soup.find_all("p",{"class":"pickup"})
        for i in name:
            item = i.string
            ilt.append(item)
        for j in name2:
            ability = j.string.strip()
            ilt2.append(ability)
    except:
        print("")
        
def printItemList(ilt, ilt2):
    len_list = [5, 20, 35]
    fmt_template = "{:%d}\t{:%d}\t{:%d}"
    def make_fmt(idx):
        return fmt_template%(len_list[0], len_list[1]-cd.get_count(ilt[idx]), len_list[2] - cd.get_count(ilt2[idx]))
    cd = ChineseDetected()
    print((fmt_template%(len_list[0]-2,len_list[1]-2, len_list[2]-2)).format("序号", "物品", "功能"))
    count = 0
    for g in range(len(ilt2)):
        count += 1
        print(make_fmt(g).format(count, ilt[g], ilt2[g]))

def main():
    infoList = []
    infoList2 = []
    url = 'http://icecat.cc/isaacab/index.html'
    html = getHTMLText(url)
    parsePage(infoList,infoList2,html)
    printItemList(infoList,infoList2)

main()
