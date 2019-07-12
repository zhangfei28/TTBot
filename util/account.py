#coding:utf-8

import json

from util.jstool import py_to_js,get_ascp
from util.tools import time_to_date
from settings import signature_js_path,signature_js_func,URL_HOST

def params_for_favourite(max_repin_time,uid=''):
    _signature = py_to_js(signature_js_path, signature_js_func, uid, max_repin_time)
    _as, _cp = get_ascp()
    return {
        'page_type': 2,
        'user_id': uid,
        'max_behot_time': 0,
        'count': 20,
        'as':_as ,
        'cp':_cp ,
        '_signature': _signature,
        'max_repin_time': max_repin_time
    }

def favourite_cleaner(item):
    item['behot_time'] = time_to_date(item.get('behot_time',0))
    item['repin_time'] = time_to_date(item.get('repin_time',0))
    item['source_url'] = URL_HOST + item.get('source_url','')
    item['media_url'] = URL_HOST + item.get('media_url', '')
    item['image_url'] = 'http:' + item.get('image_url', '')
    return item

def videos_cleaner(item):
    content = item.get('content')
    if content:
        data = json.loads(content)
        return data

def articles_cleaner(item):
    for i in ['modify_time','create_time','verify_time']:
        item['my_'+i] = time_to_date(item.get(i, 0))
    return item