import urllib
import json


class Suggester(object):
    pass
    @property
    def keyword(self):
        return self.key
    @keyword.setter
    def keyword(self, value):
        self.key = value


    @property
    def suggestions(self):
        array = []
        url = 'http://suggest-market.yandex.ru/suggest-market?srv=market&part=' + self.key + '&pos=3&_=1419492563373'
        text = urllib.urlopen(url).read().decode('utf-8')
        #text = page.read().decode('cp1251')
        c = json.loads(text)
        for i in c[1]:
            array.append(i)
        return array


s = Suggester()
s.key = 'диор'
for i in s.suggestions:
    print(i)
    
