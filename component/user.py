#coding:utf-8

from config import *
from settings import *
from util.tools import *
from component.log import getLogger
from component.dbhelper import Database
from deco import force_type
from deco.user import prepare,choose
from util.request import send_request
from util.jstool import payload_for_get
from requests.adapters import HTTPAdapter
from util.user import published_data_cleaner

logger = getLogger(__name__)

class TTUser:

    def __init__(self,uid):
        self.id = uid
        self._name = None
        self._description = None
        self._gender = None
        self._fans_count = None
        self._homepage = None
        self._info = None
        self._mid = None
        self._avatar = None
        self._follow_count = None
        self.headers_article = None
        self.db = Database(MONGODB)
        self.url_home = URL_USER_HOME.format(id=self.id)
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=MAX_RETRY))
        self.session.mount('https://', HTTPAdapter(max_retries=MAX_RETRY))

    @property
    def homepage(self):
        if self._homepage is None:
            response = send_request('get',self.url_home,session=self.session,
                                    headers=HEADERS,retries=-1)
            self._homepage = response.text
        return self._homepage

    @property
    def info(self):
        if not self._info:
            infos = find_by_pattern(self.homepage,PATTERN_USERINFO,sub_pattern='\n')
            relation = find_by_pattern(self.homepage,PATTERN_RELATION,sub_pattern='\n')
            infos = replace_by_list(infos,['false','true','\n','\'',' '],['false','true','','"',''])
            relation = replace_by_list(relation,['\n','\'',' '],['','"',''])
            infos = dict_str_to_json(infos)
            relation = dict_str_to_json(relation)
            self._info =  infos
            self._info.update(relation)
        return self._info

    @property
    def name(self):
        self._name = self.info.get('name') if not self._name else self._name
        return self._name

    @property
    def mediaId(self):
        self._mid = self.info.get('mediaId') if not self._mid else self._mid
        return self._mid

    @property
    def avatar(self):
        self._avatar = 'http:'+self.info.get('avatarUrl') if not self._avatar else self._avatar
        return self._avatar

    @property
    def follow_count(self):
        self._follow_count = int(self.info.get('guanzhu')) if not self._follow_count else self._follow_count
        return self._follow_count

    @property
    def fans_count(self):
        self._fans_count = int(self.info.get('fensi')) if not self._fans_count else self._fans_count
        return self._fans_count

    @property
    def csrftoken(self):
        return find_by_pattern(self.homepage,PATTERN_CRSFTOKEN)

    @prepare
    @force_type({'MDB':Database,'STRONG':bool,'ALL':bool,'count':int})
    def get_published(self,count=COUNT_NEWS,ALL=False,MDB=None,
                      STRONG=True,MODE=ARTICLE,**kwargs):
        hot_time = '0'
        amount = 0
        results = []
        retries = MAX_RETRY
        API = kwargs.get('API',API_USER_ARTICLE)
        headers = kwargs.get('headers',self.headers_article)
        cleaner = kwargs.get('cleaner',published_data_cleaner)
        callback = kwargs.get('data_cb')
        cb_args = kwargs.get('cb_args',())
        while 1:
            if MODE == WEITT:
                W_PARAMS.update({
                    'visit_user_id':self.id,
                    'max_behot_time':hot_time,
                })
                params = W_PARAMS
            else:
                params = payload_for_get(self.id,MODE,hot_time)
            response = send_request('get',API,
                                    session=self.session,
                                    params=params,
                                    JSON=True,
                                    retries=retries,
                                    DATA=STRONG,
                                    headers=headers)
            data = response.get('data')
            if bool(data):
                next = response.get('next')
                hot_time = next.get('max_behot_time')
                for item in data:
                    if callback and callable(callback):
                        res = callback(item,*cb_args)
                        if res:
                            continue
                    amount += 1
                    if not ALL:
                        if amount > count:
                            logger.info(f'[采集完毕] 已达到采集要求的{count}条{MODE_MAP[MODE]}数据.[OK]')
                            return results
                    if MDB:
                        tname = f'{self.name}-{self.id}'
                        item_id = item.get('item_id')
                        if MODE != WEITT:
                            asks = MDB.select({'item_id':{"=":item_id}},tname=tname)
                        else:
                            _key = 'concern_talk_cell'
                            cell = item.get(_key)
                            if not cell:
                                cell = item.get('stream_cell')
                            if cell:
                                _id = cell.get('id')
                                asks =  MDB.select({'wid':{"=":_id}},tname=tname)
                            else:
                                asks = None
                        if asks:
                            continue
                        MDB.save(item,tname=tname,format=cleaner)
                    results.append(item)
                logger.info(f'此次已采集用户:{self.name} ID:{self.id} {MODE_MAP[MODE]}数据 {amount} 条.')
            if response.get('has_more',False) is True:
                retries = -1
            else:
                logger.info(f'用户:{self.name} ID:{self.id} 此次采集{MODE_MAP[MODE]}完毕. 此次采集总数:{amount}.')
                return

    @choose('followings',api=API_USER_FOLLOWING)
    @force_type({ 'ALL': bool, 'count': int})
    def get_followings(self,count=COUNT_FOLLOWING,MDB=None,ALL=True):
        if self.follow_count == 0:
            logger.info(f'用户 {self.name} ID：{self.id} 暂时没有关注任何人.')
            return
        return {
            'count':count,
            'MDB':MDB,
            'ALL':ALL,
        }

    @choose('fans', api=API_USER_FANS)
    @force_type({ 'ALL': bool, 'count': int})
    def get_fans(self,count=COUNT_FANS,MDB=None,ALL=True):
        if self.fans_count == 0:
            logger.info(f'用户 {self.name} ID：{self.id} 暂时没有粉丝.')
            return
        return {
            'count':count,
            'MDB':MDB,
            'ALL':ALL,
        }