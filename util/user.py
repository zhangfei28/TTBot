#coding:utf-8

import json

from util.tools import time_to_date
from util.jstool import py_to_js
from settings import URL_HOST,URL_ARTICLE_ITEM,\
    F_PARAMS,signature_js_path,signature_js_func

def published_data_cleaner(item):
    item['behot_time'] = time_to_date(item.get('behot_time'))
    item['image_url'] = 'http:' + item.get('image_url','')
    item['media_url'] = URL_HOST + item.get('media_url','')
    item['source_url'] = URL_HOST + item.get('source_url','')
    item['url'] = URL_ARTICLE_ITEM.format(item_id=item.get('item_id',''))
    return item

def weitt_cleaner(item):
    result = {}
    data = item.get('concern_talk_cell')
    _data = item.get('stream_cell')
    if data:
        result['wid'] = data.get('id')
        json_str = data.get('packed_json_str')
        json_data = json.loads(json_str)
        result.update(json_data)
        result['create_time'] = time_to_date(json_data.get('create_time'))
    elif _data:
        result['wid'] = _data.get('id')
        raw_data = json.loads(_data.get('raw_data'))
        result.update(raw_data)
    return result

def f_cleaner(item):
    item['open_url'] = URL_HOST + item.get('open_url')
    item['avatar_url'] = 'http:' + item.get('avatar_url')
    return item

def payload_for_relation(uid,cursor):
    F_PARAMS.update({
        'user_id': uid,
        'cursor': cursor,
        '_signature': py_to_js(signature_js_path, signature_js_func, (uid, cursor)),
    })
    return F_PARAMS

