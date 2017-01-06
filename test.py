# -*- coding: utf-8 -*-

import requests
import re
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# r = requests.get('http://www.86kongqi.com/city/nanjing.html')
r = requests.get('http://www.pm25s.com/cn/rank/', headers={"content-type":"text"})
# r = requests.get('http://pm25.in/rank')
print(r.encoding)
# r.encoding = 'utf-8'

text = r.content.decode('utf-8')

# .encode('utf-8')
# s = unicode(text)
print(type(text))

# pattern = re.compile(ur'数据更新时间：([\d]+年[\d]+月[\d]+日[\d]+时)</div>')
# pattern = re.compile(r'</div>')
# f = open('E:\\Workspace\\Python\\PM2.5-Spider\\tmp.html', 'w')
# f.write(text)
# f.close()
match = re.search(u'数据更新时间：([\d]+年[\d]+月[\d]+日[\d]+时)</div>', text)

print(match.group(1))


citylist = ['扬州', '镇江', '南京', '杭州', '苏州', '上海', '无锡', '武汉', '合肥', '厦门', '珠海', '广州', '深圳', '天津', '北京', '成都', '长沙']

for city in citylist:
    match = re.search(city + u'</a></span><span class="lv[\d]+">([\d]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="lv[\d-]+">(优|良|轻度污染|中度污染|重度污染|严重污染)</span></div>', text)

    for i in range(10):
    	print(match.group(i)),
    print("====")
