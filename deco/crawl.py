#coding:utf-8

from component.dbhelper import Database
from component.log import getLogger
from config import COUNT_HOTNEWS,MAX_RETRY,MONGODB
from util.request import send_request
from inspect import isfunction

logger = getLogger(__name__)

def crawl_helper(method='get',api=None):
    def outter(func):
        def wrapper(self,*args,**kwargs):
            res = func(self,*args,**kwargs)
            params_func = res.get('params_func')
            more        = res.get('more','has_more')
            more_out    = res.get('more_out')
            variables   = res.get('var',{})
            handler     = res.get('condition_handle',{})
            req_kwargs  = res.get('request_kwargs',{})
            args        = res.get('extra_args',{})
            res_args    = res.get('res_args',{})
            db_setup    = res.get('db_setup',{})
            var_outer   = res.get('var_outer')
            cleaner     = res.get('cleaner')
            data_out    = res.get('data_out')
            item_out    = res.get('item_out')
            item_callback = res.get('item_callback')
            data_wrap   = res.get('data_wrap',True)
            count   = kwargs.get('count',COUNT_HOTNEWS)
            MDB     = kwargs.get('MDB')
            ALL     = kwargs.get('ALL')
            var_keys    = [i for i in variables.keys()]
            var_values  = [i for i in variables.values()]
            retries = MAX_RETRY
            amount = 0
            results = []
            while 1:
                params = params_func(*var_values,**args,**res_args)
                if method.lower() == 'post':
                    req_kwargs.update({
                        'data': params
                    })
                    if 'params' in req_kwargs:
                        req_kwargs.pop('params')
                else:
                    req_kwargs.update({
                        'params':params
                    })
                    if 'data' in req_kwargs:
                        req_kwargs.pop('data')
                response = send_request(method, api,
                                        retries=retries,
                                        **req_kwargs)
                if data_wrap:
                    data = response.get(data_out).get('data') if data_out else response.get('data')
                else:
                    data = response
                if bool(data):
                    if var_outer:
                        var_values = [response.get(var_outer).get(i) for i in var_keys]
                    else:
                        var_values = [response.get(i) for i in var_keys]
                    if res_args:
                        res_args.update({
                            'response':response
                        })
                    raw_data = data.get(item_out) if item_out else data
                    if not raw_data:
                        logger.info(f'数据抓取完毕. 此次采集总数:{amount}.')
                        return results
                    for item in raw_data:
                        if item_callback and  isfunction(item_callback):
                            cb_res = item_callback(self,item)
                            if cb_res and not isinstance(cb_res,tuple):
                                continue
                            elif isinstance(cb_res,tuple) and cb_res[-1] == 200:
                                item = cb_res[0]
                        if not ALL:
                            if amount >= count:
                                logger.info(f'[采集完毕] 已达到搜索要求的{count}条数据.[OK]')
                                return results
                        if handler:
                            flags = []
                            for i in handler.keys():
                                _func = handler[i][-1]
                                _param = handler[i][0]
                                _sec_param = item.get(i)
                                if _func(_param,_sec_param):
                                    flags.append(1)
                                else:
                                    flags.append(0)
                            if all(flags):
                                logger.info(f'未满足抓取条件,略过,标识:{item.get(db_setup["ticket"])}')
                                continue
                        if MDB :
                            if isinstance(MDB,Database) and not MDB.connected:
                                MDB.connect()
                            elif not isinstance(MDB,Database):
                                MDB = Database(MONGODB)
                                MDB.connect()
                            MDB.use_db(db_setup['db'])
                            if cleaner and callable(cleaner):
                                item = cleaner(item)
                            _id = item.get(db_setup['ticket'])
                            asks = MDB.select({db_setup['ticket']: {"=": _id}}, tname=db_setup['tname'])
                            if asks:
                                continue
                            MDB.save(item, tname=db_setup['tname'])
                        results.append(item)
                        amount += 1
                    tip = f'此次抓取 数据 {amount} 条.' if not MDB else \
                        f'此次抓取 存入数据库:{db_setup.get("db")} 数据 {amount} 条.表:{db_setup.get("tname")}'
                    logger.info(tip)
                if more_out:
                    _more = response.get(more_out).get(more)
                else:
                    _more = response.get(more)
                if _more:
                    retries += 1
                else:
                    logger.info(f'数据抓取完毕. 此次采集总数:{amount}.')
                    return results
        return wrapper
    return outter

def choose(func):
    def wrapper(self,*args,**kwargs):
        cate = func(self,*args,**kwargs)
        mdb = kwargs.get('MDB')
        if mdb and not isinstance(mdb,Database):
            kwargs['MDB'] = self.db
        return self.crawl_news(cate=cate,**kwargs)
    return wrapper
