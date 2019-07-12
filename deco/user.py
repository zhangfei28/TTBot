#coding:utf-8

from util.user import *
from copy import deepcopy
from component.log import getLogger
from component.dbhelper import Database
from config import MONGODB,MAX_RETRY
from util.request import send_request
from settings import  HEADERS_USER_ARTICLE,MODE_MAP,\
    API_USER_WEITT,API_USER_ARTICLE,HEADERS,APIS

logger = getLogger(__name__)

def prepare(func):
    def wrapper(self,*args,**kwargs):
        self.headers_article = deepcopy(HEADERS_USER_ARTICLE)
        self.headers_article.update(
            {
                'referer':f'https://www.toutiao.com/c/user/{self.id}/',
            }
        )
        if not self.session.cookies:
            self.headers_article.update(
                {
                    'cookie': f'csrftoken={self.csrftoken}',
                })
        MDB = kwargs.get('MDB')
        MODE =  kwargs.get('MODE')
        MODE = '1' if not MODE else MODE
        dbname = MONGODB[MODE_MAP[MODE]]
        if MODE == '2':
            API = API_USER_WEITT
            headers = HEADERS
            cleaner = weitt_cleaner
        else:
            API = API_USER_ARTICLE
            headers = self.headers_article
            cleaner = published_data_cleaner
        if MDB :
            if isinstance(MDB,Database) and not MDB.connected:
                MDB.connect()
            elif not isinstance(MDB,Database):
                MDB = self.db
                if not MDB.connected:
                    MDB.connect()
            MDB.use_db(dbname)
            kwargs['MDB']=MDB
        kwargs['headers']=headers
        kwargs['API'] = API
        kwargs['cleaner'] = cleaner
        return func(self,*args,**kwargs)
    return wrapper

def choose(option,api=None,method='get'):
    def outter(func):
        def wrapper(self,*args,**kwargs):
            url = APIS[option] if api is None else api
            result = func(self,*args,**kwargs)
            if not result:
                return []
            count = result.get('count',0)
            amount = 0
            cursor = 0
            retries = MAX_RETRY
            results = []
            MDB = result.get('MDB')
            ALL = result.get('ALL')
            dbname = MONGODB[option]
            if MDB:
                if isinstance(MDB, Database) and not MDB.connected:
                    MDB.connect()
                elif not isinstance(MDB, Database):
                    MDB = self.db
                    if not MDB.connected:
                        MDB.connect()
                MDB.use_db(dbname)
            while 1:
                params = payload_for_relation(self.id,cursor)
                response = send_request(method, url,
                                        params=params,
                                        JSON=True,
                                        session=self.session,
                                        retries=retries,
                                        DATA=1,
                                        headers=HEADERS)
                data = response.get('data')
                if bool(data):
                    cursor = response.get('cursor')
                    for item in data:
                        if not ALL:
                            if amount >= count:
                                logger.info(f'[采集完毕] 已达到采集要求的{count}条数据.[OK]')
                                return results
                        if MDB:
                            tname = f'{self.name}-{self.id}'
                            user_id = item.get('user_id')
                            asks = MDB.select({'user_id': {"=": user_id}}, tname=tname)
                            if asks:
                                continue
                            MDB.save(item, tname=tname, format=f_cleaner)
                        results.append(item)
                        amount += 1
                    logger.info(f'此次已采集用户:{self.name} ID:{self.id} {option}数据 {amount} 条.')
                if response.get('cursor') != 0:
                    retries = -1
                else:
                    logger.info(f'用户:{self.name} ID:{self.id} 此次采集{option}完毕. 此次采集总数:{amount}.')
                    return results
        return wrapper
    return outter