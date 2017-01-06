# PM2.5-Spider
Python Spider for PM2.5 data in China.

The .db file is for the database sqlite, please use [DB Browser](http://sqlitebrowser.org/) to open it.

# Install
Just run the following command, the program just has been tested in python 3.5.

>python spider.py

# Dependencies
Need [requests](http://docs.python-requests.org/en/master/).

# The sample of the data
|RunId| City| AQI| QUALITY | PM25 | PM10 | CO | NO2 | SO2| O3-平均一小时 | O3-平均八小时 | TIME |
| :-------------: |:-------------:| :-------------:| :-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
|1|	扬州|	62|	良|	44|	59|	0.825|	37|	13|	35|	48|	2017年1月6日14时|

# Reference
The data is from [pm25s](http://www.pm25s.com/cn/rank/) and the original data is from [pm25.in](http://pm25.in/)
