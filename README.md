# PM2.5-Spider
Python Spider for PM2.5 data in China.

The .db file is for the database sqlite, please use [DB Browser](http://sqlitebrowser.org/) to open it.

# Install
Just run the following command, the program has just been tested in python 3.5.

>python spider.py

# Dependencies
Need [requests](http://docs.python-requests.org/en/master/).

# The sample of the data
Get the PM2.5 data for the following cities:

>['扬州', '镇江', '南京', '杭州', '苏州', '上海', '无锡', '武汉', '合肥', '厦门', '珠海', '广州', '深圳', '天津', '北京', '成都', '长沙']

|RunId| CITY| AQI| QUALITY | PM25 | PM10 | CO | NO2 | SO2| O3-平均1h | O3-平均8h | TIME |
| :-------------: |:-------------:| :-------------:| :-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
|1|	扬州|	62|	良|	44|	59|	0.825|	37|	13|	35|	48|	2017年1月6日14时|

# Reference
The data is from [pm25s](http://www.pm25s.com/cn/rank/) and the original data is from [pm25.in](http://pm25.in/).
