#coding:utf-8

import time
import requests
from config import *
from settings import URL_HOST,HEADERS
from util.proxy import get_proxy
from component.log import getLogger

logger = getLogger(__name__)

def send_request(method,
                 url,
                 session=None,
                 JSON=False,
                 DATA=False,
                 retries=MAX_RETRY,
                **kwargs):
    proxy_on = False
    if method.lower() not in HTTP_METHODS:
        raise Exception(f'非法请求操作:{method}.')
    if session is None:
        session = requests.session()
    if retries == -1:
        attempt = -1
    elif retries == 0:
        attempt = 1
    else:
        attempt = retries + 1
    while attempt != 0:
        try:
            response = session.request(method,url,**kwargs)
            code = response.status_code
        except Exception as e:
            logger.error(f'[请求异常]{e.__class__.__name__}:{e}')
            kwargs['proxies'] = get_proxy()
            proxy_on = True
            attempt -= 1
            continue
        if code not in OK_CODE :
            logger.error(f'[{code}]非正常请求页面.使用代理重试中.')
            kwargs['proxies'] = get_proxy()
            proxy_on = True
            attempt -= 1
            continue
        if JSON:
            try:
                response = response.json()
            except Exception as e:
                logger.error(f'[无效json格式]{e.__class__.__name__}:{e}')
                if proxy_on:
                    kwargs['proxies'] = get_proxy()
                attempt -= 1
                continue
            else:
                if DATA:
                    data = response.get('data')
                    next = response.get('next')
                    cursor = response.get('cursor')
                    has_more = response.get('has_more')
                    if cursor == 0 or cursor:
                        return response
                    if not bool(data) and not next:
                        if has_more is 0:
                            return response
                        logger.debug(f'[无数据返回]:{response}')
                        if response == {}:
                            # r = requests.get(URL_HOST, headers=HEADERS)
                            # cookie = r.cookies.get('tt_webid')
                            # kwargs['cookies'] = {'tt_webid':cookie}
                            # continue
                            return response
                        if proxy_on:
                            kwargs['proxies'] = get_proxy()
                        attempt -= 1
                        continue
        time.sleep(DELAYS)
        return response