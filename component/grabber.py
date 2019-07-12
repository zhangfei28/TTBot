#coding:utf-8
import time
import queue

from config import *
from settings import ARTICLE,VIDEO,WEITT
from component.log import getLogger
from component.dbhelper import Database
from component.user import TTUser
from util.thread import GrabThread
from util.tools import time_to_date

logger = getLogger(__name__)

class UserGrabber:

    def __init__(self):
        self.db = Database(MONGODB)
        self.ID_queue = queue.LifoQueue()

    def __grab(self,uid,mode):
        if not self.db.connected:
            self.db.connect()
        check = self.db.select({
            'uid':uid,
            'mode':mode,
        },tname=FINISHED_TABLE,c_map=False)
        if check:
            logger.info(f'当前用户uid:{uid} 已经被爬取过 [{check[0].get("done_time")}].')
            return 1
        user = TTUser(uid)
        followings = user.get_followings(MDB=1)
        for i in followings:
            self.ID_queue.put_nowait(i.get('user_id'))
        logger.info(f'加载 用户ID：{uid} 关注的uid {len(followings)} 个进入队列.')
        logger.info(f'开始爬取用户ID：{uid} 的头条数据.MODE[{mode}]')
        if mode in [ARTICLE,VIDEO,WEITT]:
            user.get_published(ALL=True,MDB=1,MODE=mode)
        elif mode == 'all':
            for i in [ARTICLE,VIDEO,WEITT]:
                user.get_published(ALL=True, MDB=1, MODE=i)
        else:
            raise ValueError(f'头条用户链式抓取模式 mode 参数值错误:{mode}')
        self.db.save({
            'uid':uid,
            'mode':mode,
            'done_time':time_to_date(time.time()),
        },tname=FINISHED_TABLE)
        return 1

    def run_forever(self,mode=ARTICLE):
        if self.ID_queue.empty():
            self.ID_queue.put_nowait(ENTER_USER_ID)
        while 1:
            if not self.ID_queue.empty():
                uids = []
                threads = []
                res = []
                for i in range(MAX_THREADS):
                    try:
                        uids.append(self.ID_queue.get_nowait())
                    except:
                        break
                logger.info(f'已装载 {len(uids)} 个uid进入队列.')
                for _,uid in enumerate(uids):
                    threads.append(GrabThread(self.__grab,args=(uid,mode)))
                for i in threads:
                    i.start()
                for i in threads:
                    i.join()
                    res.append(i.get_result())
                count = sum([i for i in res if isinstance(i,int)])
                logger.info(f'此次抽取队列uid爬取任务 实际完成 {count} 个.')