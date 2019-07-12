#coding:utf-8

from util.jstool import py_to_js,get_ascp
from util.tools import time_to_date
from settings import signature_js_func,signature_js_path,ascp_js_func,ascp_js_path,URL_HOST

def params_for_news(max_behot_time,category='news_hot'):
    _signature = py_to_js(signature_js_path, signature_js_func,'', max_behot_time)
    # ascp = py_to_js(ascp_js_path, ascp_js_func)
    _as, _cp = get_ascp()
    # _as,_cp = ascp['as'],ascp['cp']
    params = {
        'category': category,
        'utm_source': 'toutiao',
        'widen': 1,
        'max_behot_time': max_behot_time,
        'max_behot_time_tmp': max_behot_time,
        'tadrequire': 'true',
        'as': _as,
        'cp': _cp,
       '_signature': _signature,
    }
    return params

def data_cleaner(item):
    item['media_url'] = URL_HOST + item.get('media_url','')
    item['source_url'] = URL_HOST + item.get('source_url','')
    item['behot_time'] = time_to_date(item.get('behot_time'))
    item['media_avatar_url'] = 'http:' + item.get('media_avatar_url','')
    item['image_url'] = 'http:' + item.get('image_url', '')
    return item
