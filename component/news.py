#coding:utf-8

import time
import requests

from component.dbhelper import Database
from deco.crawl import crawl_helper,choose
from util.news import params_for_news,data_cleaner
from util.tools import time_to_date
from config import COUNT_HOTNEWS,MONGODB
from settings import API_NEWS_FEED,HEADERS,URL_HOST

class TTNews:

    def __init__(self):
        self.db = Database(MONGODB)

    @property
    def tt_webid(self):
        r = requests.get(URL_HOST, headers=HEADERS)
        return r.cookies.get('tt_webid')

    @crawl_helper(api=API_NEWS_FEED)
    def crawl_news(self, last_time=None,
                   count=COUNT_HOTNEWS, ALL=True, MDB=None, cate='news_hot'):

        def deadline_out(last_time_raw,time_by_minute):
            if last_time_raw is None:
                return
            ctime = time_to_date(time_by_minute)
            if ctime <= last_time_raw:
                return True

        return {
            'params_func':params_for_news,
            'var':{
                'max_behot_time':0,
            },
            'condition_handle':{
                'behot_time':[last_time,deadline_out],
            },
            'request_kwargs':{
                'headers':HEADERS,
                'JSON':True,
                'DATA':1,
                'cookies':{'tt_webid':self.tt_webid}
            },
            'db_setup':{
                'tname': f'{cate}_{time_to_date(int(time.time()),format="%Y-%m-%d")}',
                'db':MONGODB[cate],
                'ticket':'item_id',
            },
            'extra_args':{
                'category':cate,
            },
            'more':'next',
            'var_outer':'next',
            'cleaner':data_cleaner,
        }

    @choose
    def get_recommend_news(self, last_time=None,
                     count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return '__all__'

    @choose
    def get_hot_news(self, last_time=None,
                     count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_hot'

    @choose
    def get_entertainment_news(self, last_time=None,
                               count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_entertainment'

    @choose
    def get_tech_news(self, last_time=None,
                      count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_tech'

    @choose
    def get_game_news(self, last_time=None,
                      count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_game'

    @choose
    def get_sports_news(self, last_time=None,
                        count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_sports'

    @choose
    def get_car_news(self, last_time=None,
                     count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_car'

    @choose
    def get_finance_news(self, last_time=None,
                         count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_finance'

    @choose
    def get_internet_news(self, last_time=None,
                          count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'internet'

    @choose
    def get_software_news(self, last_time=None,
                          count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'software'

    @choose
    def get_smart_device_news(self, last_time=None,
                              count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return '智能家居'

    @choose
    def get_movie_news(self, last_time=None,
                       count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'movie'

    @choose
    def get_TV_play_news(self, last_time=None,
                         count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return '电视剧'

    @choose
    def get_shows_news(self, last_time=None,
                       count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return '综艺'

    @choose
    def get_gossip_news(self, last_time=None,
                        count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'gossip'

    @choose
    def get_NBA_news(self, last_time=None,
                     count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'NBA'

    @choose
    def get_CBA_news(self, last_time=None,
                     count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'CBA'

    @choose
    def get_CSL_news(self, last_time=None,
                     count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return '中超'

    @choose
    def get_ISA_news(self, last_time=None,
                     count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'football_italy'

    @choose
    def get_SUV_news(self, last_time=None,
                     count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'SUV'

    @choose
    def get_car_new_arrival_news(self, last_time=None,
                                 count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'car_new_arrival'

    @choose
    def get_car_guide_news(self, last_time=None,
                           count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'car_guide'

    @choose
    def get_car_usage_news(self, last_time=None,
                           count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'car_usage'

    @choose
    def get_investment_news(self, last_time=None,
                            count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'investment'

    @choose
    def get_stock_news(self, last_time=None,
                       count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'stock'

    @choose
    def get_finance_management_news(self, last_time=None,
                                    count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'finance_management'

    @choose
    def get_macro_economic_news(self, last_time=None,
                                count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'macro_economic'

    @choose
    def get_military_news(self, last_time=None,
                          count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_military'

    @choose
    def get_china_military_news(self, last_time=None,
                                count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'military_china'

    @choose
    def get_world_military_news(self, last_time=None,
                                count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'military_world'

    @choose
    def get_weaponry_news(self, last_time=None,
                          count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'weaponry'

    @choose
    def get_funny_news(self, last_time=None,
                       count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'funny'

    @choose
    def get_fashion_news(self, last_time=None,
                         count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_fashion'

    @choose
    def get_dress_news(self, last_time=None,
                       count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return '时装'

    @choose
    def get_wristwatch_news(self, last_time=None,
                            count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return '腕表'

    @choose
    def get_jewellery_news(self, last_time=None,
                           count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return '珠宝'

    @choose
    def get_body_shape_news(self, last_time=None,
                            count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return '美体'

    @choose
    def get_food_news(self, last_time=None,
                      count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_food'

    @choose
    def get_good_article_news(self, last_time=None,
                              count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_essay'

    @choose
    def get_child_news(self, last_time=None,
                       count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_baby'

    @choose
    def get_travel_news(self, last_time=None,
                        count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_travel'

    @choose
    def get_world_news(self, last_time=None,
                       count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_world'

    @choose
    def get_history_news(self, last_time=None,
                         count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_history'

    @choose
    def get_regimen_news(self, last_time=None,
                         count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_regimen'

    @choose
    def get_discovery_news(self, last_time=None,
                           count=COUNT_HOTNEWS, ALL=True, MDB=None):
        return 'news_discovery'
