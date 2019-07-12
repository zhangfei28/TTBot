#coding:utf-8

import os
import random
import requests
from config import *
from w3lib.url import is_url

def gen_proxy(proxy):
    proxy = proxy.strip('\n')
    return {
        'http':f'http://{proxy}',
        'https': f'https://{proxy}',
    }

def get_proxy():
    if not PROXY_ENABLE:
        return
    if PROXY:
        if not is_url(PROXY):
            return gen_proxy(PROXY)
    if is_url(PROXY_POOL):
        p = requests.get(PROXY_POOL).text.strip('\r\n')
        return gen_proxy(p)
    if os.path.isfile(PROXY_POOL):
        with open(PROXY_POOL,'r') as f:
            p_txt = f.readlines()
        return random.choice([gen_proxy(i) for i in p_txt])
    if isinstance(PROXY_POOL,list):
        return random.choice([gen_proxy(i) for i in PROXY_POOL])
    return None