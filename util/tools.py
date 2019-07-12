#coding:utf-8

import re
import json
import time
import requests

from urllib3 import encode_multipart_formdata

def find_by_pattern(src,pattern,index=0,ALL=False,sub_pattern=None,sub_str=''):
    results = re.findall(pattern,src)
    if results:
        if not ALL:
            result = results[index]
            result = re.sub(sub_pattern,sub_str,result) if sub_pattern else result
            return result
        if sub_pattern:
            results = [re.sub(sub_pattern,sub_str,i) for i in results]
        return results

def replace_by_list(src,str_list,re_list):
    for _,i in enumerate(str_list):
        src = src.replace(i,re_list[_])
    return src

def dict_str_to_json(src):
    _ = []
    src = re.sub('[{}]','',src)
    for item in src.split(','):
        a,b = item.split(':')
        _.append('"'+a+'"'+":"+b)
    res  = '{'+','.join(_)+'}'
    res = json.loads(res)
    return res

def format_cookies(cookie_dict):
    res = []
    names = []
    for i in cookie_dict:
        name = i.get('name')
        if name in names:
            continue
        value = i.get('value')
        res.append('='.join([name,value]))
        names.append(name)
    return ';'.join(res)

def post_files(url,header,data,filename,filepath):
    data['file']= (filename,open(filepath,'rb').read())
    encode_data = encode_multipart_formdata(data)
    data = encode_data[0]
    header['Content-Type'] = encode_data[1]
    r = requests.post(url, headers=header, data=data)
    return r

def time_to_date(timestamp,format="%Y-%m-%d %H:%M:%S"):
	"""
	:usage:
		时间戳转换为日期
	:param data:
		@timestamp		：时间戳，int类型，如：1537535021
	:return:
		@otherStyleTime ：转换结果日期，格式： 年-月-日 时:分:秒
	"""
	timearr = time.localtime(timestamp)
	otherStyleTime = time.strftime(format, timearr)
	return  otherStyleTime

def datetime_to_timestamp(datetime,format='%Y-%m-%d %H:%M:%S'):
    timeArray = time.strptime(datetime, format)
    ts = int(time.mktime(timeArray))
    return ts






