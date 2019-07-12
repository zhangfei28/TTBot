#coding:utf-8

import os

from component.log import getLogger
from component.dbhelper import Database
from util.request import send_request
from config import COOKIE_FILE,COOKIE
from inspect import isfunction

logger = getLogger(__name__)

def check(func):
    def wrapper(self,*args,**kwargs):
        cookie = 0
        if COOKIE:
            cookie = COOKIE
        elif os.path.exists(COOKIE_FILE):
            try:
                with open(COOKIE_FILE,'r') as f:
                    cookie = f.read()
            except Exception as e:
                logger.error(f'{e}')
                return func(self, *args, **kwargs)
        if not cookie:
            return func(self,*args,**kwargs)
        self.login_headers = {
            'cookie': cookie
        }
    return wrapper

def login_required(func):
    def wrapper(self,*args,**kwargs):
        if self.login_headers is None:
            self.login()
        return func(self,*args,**kwargs)
    return wrapper

def choose(func):
    def wrapper(self,*args,**kwargs):
        cate = func(self,*args,**kwargs)
        mdb = kwargs.get('MDB')
        if mdb and not isinstance(mdb,Database):
            kwargs['MDB'] = self.db
        return self.new_crawler.crawl_news(cate=cate,**kwargs)
    return wrapper

def action(method,api):
    def outer(func):
        def wrapper(self,*args,**kwargs):
            res = func(self,*args,**kwargs)
            params = res.get('params')
            API = res.get('api',api)
            if API is None:
                API = api
            _ = {
                'get':'params',
                'post':'data',
            }[method.lower()]
            p = {_:params}
            extra_kwargs = res.get('extra_kwargs')
            p.update(extra_kwargs)
            response = send_request(method.lower(),
                                    url=API,
                                    session=self.session,
                                    **p)
            if response:
                msg = res.get('msg')
                check_func = res.get('check_func')
                tips = res.get('tips',{})
                callback = res.get('callback')
                if msg:
                    keys = [i for i in msg.keys()]
                    if all([response.get(i)==msg[i] for i in keys]):
                        logger.info(tips.get('ok'))
                    else:
                        logger.info(tips.get('fail'))
                elif check_func:
                    res = check_func(response)
                    if res:
                        logger.info(tips.get('ok'))
                    else:
                        logger.info(tips.get('fail'))
                if callback and isfunction(callback):
                    return callback(self,response)
            return response
        return wrapper
    return outer

def to_do(func):
    def wrapper(self,*args,**kwargs):
        return func(self,*args,**kwargs)
    return wrapper
