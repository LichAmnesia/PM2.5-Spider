# -*- coding: utf-8 -*-
# @Author: Lich_Amnesia
# @Date:   2017-01-05 23:34:12
# @Last Modified by:   Lich_Amnesia
# @Last Modified time: 2017-01-06 00:49:03
# @Email: shen.huang@colorado.edu

import json
import sqlite3
import requests
import re
import datetime
import time
import sys
import os
import random


class PM25Fetch(object):
    """docstring for PM25Fetch"""

    def __init__(self, arg=None, filename=None, quiet=False):
        super
        (PM25Fetch, self).__init__()
        self.arg = arg
        # Sqlite
        self.con = sqlite3.connect(filename)
        try:
            self.create_table()
        except Exception as e:
            if re.match(r'table .* already exists', str(e)):
                print("table already exists")
            else:
                raise e
        else:
            print("create table PM25City successfully")
        # requests
        self.s = requests.Session()
        self.fileds = ['RunID', 'CITY', 'AQI', 'QUALITY', 'PM25',
                       'PM10', 'CO', 'NO2', 'SO2', 'O3-1', 'O3-8', 'TIME']
        self.citylist = ['扬州', '镇江', '南京', '杭州', '苏州', '上海', '无锡', '武汉', '合肥', '厦门', '珠海', '广州', '深圳', '天津', '北京', '成都', '长沙']

    def create_table(self):
        cu = self.con.cursor()
        cu.execute('''CREATE TABLE [PM25City] (
              [RunID] integer NOT NULL ON CONFLICT REPLACE PRIMARY KEY,
              [CITY] varchar(40),
              [AQI] integer,
              [QUALITY] varchar(40),
              [PM25] integer,
              [PM10] integer,
              [CO] real,
              [NO2] integer,
              [SO2] integer,
              [O3-1] integer,
              [O3-8] integer,
              [TIME] varchar(50));
        ''')
        cu.execute('CREATE INDEX [RunID] ON [PM25City] ([RunID] ASC);')
        cu.close()

    # 获取网页信息，返回response
    def fetch_html(self, url):
        while True:
            success = True
            print("[{0}] fetch ok ".format(time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime())))
            try:
                resp = self.s.get(url, timeout=5, verify=False)
            except Exception as e:
                print(str(e))
                success = False
                time.sleep(5)
            else:
                print("[{0}] status code: {1}".format(time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime()), resp.status_code))
                if resp.status_code != 200:
                    success = False
                    time.sleep(5)
            if success:
                break
        return resp

    def fetch(self):
        baseurl = "http://www.pm25s.com/cn/rank/"
        
        resp = self.fetch_html(baseurl)
        # result = urllib2.urlopen(yql_url).read()
        data = resp.content
        data = data.decode('utf-8')
        get_time = re.search(u'数据更新时间：([\d]+年[\d]+月[\d]+日[\d]+时)</div>', data).group(1)
        # check the data for this time exists or not?
        if get_time == self.getTime():
            print("The time {0} exists, will wait for next time update.".format(get_time))
            return 

        for city in self.citylist:
            match = re.search(city + u'</a></span><span class="lv[\d]+">([\d]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="aqis">([\d.-]+)</span><span class="lv[\d-]+">(优|良|轻度污染|中度污染|重度污染|严重污染)</span></div>', data)

            ans_list = [0]
            for i in range(1, 10):
                if match.group(i) == '-':
                    ans_list.append(None)
                else:
                    ans_list.append(match.group(i))
            
            AQI = int(ans_list[1]) if ans_list[1] != None else None
            Quality = ans_list[9] if ans_list[9] != None else None
            PM25 = int(ans_list[2]) if ans_list[2] != None else None
            PM10 = int(ans_list[3]) if ans_list[3] != None else None
            CO = float(ans_list[4]) if ans_list[4] != None else None
            NO2 = int(ans_list[5]) if ans_list[5] != None else None
            SO2 = int(ans_list[6]) if ans_list[6] != None else None
            O31 = int(ans_list[7]) if ans_list[7] != None else None
            O38 = int(ans_list[8]) if ans_list[8] != None else None
            
            line = {
                'RunID': self.getRunID(),
                'CITY': city,
                'AQI': AQI,
                'QUALITY': Quality,
                'PM25': PM25,
                'PM10': PM10,
                'CO': CO,
                'NO2': NO2,
                'SO2': SO2,
                'O3-1': O31,
                'O3-8': O38,
                'TIME': get_time,
            }

            print('[{2}] RunID = {0}. Got {1} fields at {3}. The city is {4}'.format(line['RunID'], len(line), time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime()), get_time, city))
            self.insert(line)
        
        return 

    def getRunID(self):
        RunID = 1
        cu = self.con.cursor()
        cu.execute("SELECT RunID from PM25City ORDER by RunID DESC LIMIT 1")
        bk = cu.fetchone()
        if bk is None or len(bk) == 0:
            RunID = 1
        else:
            RunID = bk[0] + 1
        return RunID

    # Check the time exist or not
    def getTime(self):
        res_time = None
        cu = self.con.cursor()
        cu.execute("SELECT TIME from PM25City ORDER by RunID DESC LIMIT 1")
        bk = cu.fetchone()
        if bk is None or len(bk) == 0:
            res_time = None
        else:
            res_time = bk[0]
        return res_time

    def insert(self, status):
        cu = self.con.cursor()
        status_array = []
        s = []
        for key in self.fileds:
            s.append(status[key])
        status_array.append(s)
        cu.executemany(
            'INSERT OR REPLACE INTO PM25City Values(?,?,?,?,?,?,?,?,?,?,?,?)', status_array)
        self.con.commit()

    def print_ts(self, message):
        print("[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))

    def run(self, begin, end):
        self.print_ts("-" * 60)
        self.print_ts("Starting by {0} to {1} seconds.".format(begin, end))
        self.print_ts("-" * 60)
        while True:
            try:
                interval = random.randint(begin, end)
                # sleep for the remaining seconds of interval
                time_remaining = interval
                self.print_ts("Sleeping until %s (%s seconds)..." % (
                    (time.ctime(time.time() + time_remaining)), time_remaining))
                time.sleep(time_remaining)
                self.print_ts("Starting command.")
                # execute the command
                self.fetch()
                self.print_ts("-" * 60)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    filename = "pm25city.db"
    fetcher = PM25Fetch(filename=filename)
    begin = 3300
    end = 3589
    fetcher.run(begin, end)