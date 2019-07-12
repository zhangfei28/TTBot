#coding:utf-8

import copy
import time

from component.log import getLogger
from component.dbhelper import Database
from component.sliderlogin import SliderHelper
from settings import API_SEARCH,HEADERS,URL_SEARCH_TEST
from util.request import send_request
from util.search import params_for_search
from config import SVWEBID,COUNT_SEARCH,SVWEBID_FILE,\
    MAX_RETRY,MONGODB,IMG_S_BIG_PATH,IMG_S_BLOCK_PATH

logger = getLogger(__name__)

class Searcher:

    def __init__(self):
        self.headers = copy.deepcopy(HEADERS)
        self.headers['cookie'] = SVWEBID
        self.slider = SliderHelper()

    def search(self,keyword,count=COUNT_SEARCH,
               USER=False,VIDEO=False,ALL=True,
               MDB=None,strict=False):
        if USER:
            tab = 4
        elif VIDEO:
            tab = 2
        else:
            tab = 1

        tab_kind = {
            1:'综合',
            2:'视频',
            4:'用户'
        }

        amount = 0
        offset = 0
        results = []
        retries = MAX_RETRY
        dbname = MONGODB['search']

        if MDB :
            if isinstance(MDB, Database) and not MDB.connected:
                MDB.connect()
            elif not isinstance(MDB,Database):
                MDB = Database(MONGODB)
                MDB.connect()
            MDB.use_db(dbname)
        while 1:
            params = params_for_search(keyword,tab=tab,offset=offset)
            response = send_request('get',API_SEARCH,
                                    params=params,
                                    JSON=True,
                                    retries=retries,
                                    DATA=1,
                                    headers=self.headers)
            data = response.get('data')
            if bool(data):
                offset = response.get('offset')
                for item in data:
                    if not ALL:
                        if amount >= count:
                            logger.info(f'[采集完毕] 已达到搜索要求的{count}条数据.[OK]')
                            return results
                    if MDB:
                        tname = f'{keyword}-{tab_kind[tab]}'
                        _id = item.get('id')
                        asks = MDB.select({'id': {"=": _id}}, tname=tname)
                        if asks:
                            continue
                        MDB.save(item, tname=tname)
                    if strict and USER:
                        name = item.get('name')
                        if name == keyword:
                            logger.info(f'[搜索匹配成功]Strict 模式下搜索到相关用户!')
                            return item
                    results.append(item)
                    amount += 1
                logger.info(f'此次已搜索:{keyword} {tab_kind[tab]}数据 {amount} 条.')
            if response.get('has_more') != 0:
                retries = -1
            else:
                logger.info(f'搜索关键词:{keyword} {tab_kind[tab]}数据采集完毕. 此次采集总数:{amount}.')
                return results

    def validate(self):
        self.slider.init_chrome()
        self.slider.driver.get(URL_SEARCH_TEST)
        time.sleep(2)
        self.slider._slider_img_download(big_path=IMG_S_BIG_PATH,block_path=IMG_S_BLOCK_PATH)
        self.slider._validate_and_drag(big_path=IMG_S_BIG_PATH,block_path=IMG_S_BLOCK_PATH)
        cookie = self.slider.driver.get_cookie('s_v_web_id')
        self.headers['cookie'] = f'{cookie.get("name")}={cookie.get("value")}'
        logger.info(f'搜索滑动识别成功，验证cookie:{self.headers["cookie"]}')
        self.slider.stop()
        with open(SVWEBID_FILE,'w') as f:
            f.write(self.headers['cookie'])