#coding:utf-8

import time

from component.log import getLogger
from deco import force_type
from util.tools import time_to_date,datetime_to_timestamp

logger = getLogger(__name__)

class Timer:

    def __init__(self):
        self.jobs = {}

    @force_type({'kwargs':dict,'args':tuple})
    def setup(self,timer_time,
              timer_func,
              args=None,
              kwargs=None,
              looping=False,
              frequency=1,
              args_func=None,
              kwargs_func=None,
              callback=None,
              ):
        """
        :param timer_time: 什么时候执行 格式：'2019-07-06 15:10:00'
        :param timer_func: 时间点到了执行的函数
        :param args: 调用的函数所需要的参数,元组格式
        :param kwargs: 调用的参数所需要的键值对参数，dict格式
        :param looping:是否循环进行互动，即每隔一个周期进行检测相关条件，符合条件则进行互动
        :param frequency: 互动频率，一小时内进行多少次互动函数调用
        :param args_func: 每次调用后函数元组参数的更改回调参数
        :param kwargs_func: 每次调用后函数键值对参数的更改回调参数
        :param callback: 函数执行后的回调函数
        """
        new_item = {
            'func':timer_func,
            'args':args,
            'kwargs':kwargs,
            'callback':callback,
            'looping':looping,
            'frequency':frequency,
            'args_func':args_func,
            'kwargs_func':kwargs_func
        }
        if timer_time in self.jobs:
            value = self.jobs[timer_time]
            if isinstance(value,tuple):
                self.jobs.update({
                    timer_time:(new_item,) + value
                })
            elif isinstance(value,list):
                self.jobs.update({
                    timer_time:tuple(value) + (new_item,)
                })
            elif isinstance(value,dict):
                self.jobs.update({
                    timer_time:(value,new_item,)
                })
        else:
            self.jobs.update({
                timer_time:new_item,
            })

    def run(self):
        while 1:
            ctime = time_to_date(time.time())
            pops = []
            adds = []
            for k,v in self.jobs.items():
                if k <= ctime:
                    if isinstance(v,dict):
                        v = [v]
                    for func_entry in v:
                        kwargs = func_entry.get('kwargs')
                        args = func_entry.get('args')
                        func = func_entry.get('func')
                        kwargs = {} if not kwargs else kwargs
                        args = () if not args else args
                        res = func(*args,**kwargs)
                        callback = func_entry['callback']
                        if callback and callable(callback):
                            callback(res)
                        looping = func_entry.get('looping')
                        frequency = func_entry.get('frequency')
                        args_func = func_entry.get('args_func')
                        kwargs_func = func_entry.get('kwargs_func')
                        if looping:
                            if args_func and callable(args_func):
                                args = args_func(args)
                            if kwargs_func and callable(kwargs_func):
                                kwargs = kwargs_func(kwargs)
                            k_ts = datetime_to_timestamp(k)
                            offset_time = 3600/int(frequency)
                            next_time = time_to_date(k_ts+offset_time)
                            adds.append({
                                next_time:{'func':func,'args':args,
                                             'kwargs':kwargs,'callback':callback,
                                             'looping':looping,'frequency':frequency,
                                             'args_func': args_func, 'kwargs_func': kwargs_func
                                           }
                            })
                    pops.append(k)
                    logger.info(f'定时器任务 时间:{k} {len(v)}个 已经完成. ')
            for k in pops:
                self.jobs.pop(k)
            for i in adds:
                self.jobs.update(i)
                logger.info(f'新增定时器任务:{i.keys()}')
            if not self.jobs:
                logger.info(f'定时器任务已全部执行完毕,退出定时器.')
                return