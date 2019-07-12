#coding:utf-8

import time
from deco import force_type

@force_type({'tab':int})
def params_for_search(keyword,tab=1,offset=0,count=20):
    cur_tab = {
        1:('search_tab','synthesis'),
        2:('video','video'),
        4:('media','user'),
    }
    params = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': count,
        'en_qc': 1,
        'cur_tab': tab,
        'from': cur_tab[tab][0],
        'pd': cur_tab[tab][1],
        'timestamp': f'{int(time.time()*1000)}',
    }
    return params